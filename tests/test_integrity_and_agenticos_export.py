import importlib.util
import json
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


integrity = load_module("skills_brain_integrity", ROOT / "tooling" / "integrity.py")
agenticos_export = load_module("agenticos_export", ROOT / "adapters" / "agenticos" / "export.py")


def write_skill(root: Path, *, formatting_variant: bool = False):
    root.mkdir(parents=True)
    (root / "SKILL.md").write_text("---\nname: demo\n---\n# Demo\n", encoding="utf-8")
    manifest = {
        "schema_version": "2.1",
        "id": "demo-skill",
        "version": "1.0.0",
        "status": "candidate",
        "description": "Demo skill",
        "capabilities": ["verification.audit"],
        "requirements": {"tool_capabilities": ["filesystem.read"]},
        "risk": {"level": 1},
        "side_effects": "none",
        "security": {
            "network": {"outbound": False},
            "filesystem": {"read": True, "write": False},
            "shell": False,
            "destructive_operations": False,
        },
        "evaluation": {"golden_tasks": "optional", "minimum_score": 0.8},
        "ownership": {"maintainer": "skills-brain"},
        "provenance": {"origin": "skills-brain"},
    }
    if formatting_variant:
        text = yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=120)
    else:
        text = yaml.safe_dump(manifest, sort_keys=True, allow_unicode=True)
    (root / "skill.yaml").write_text(text, encoding="utf-8")
    return manifest


def test_manifest_hash_ignores_yaml_formatting_and_integrity_field(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    write_skill(a, formatting_variant=False)
    manifest = write_skill(b, formatting_variant=True)
    manifest["integrity"] = {"package_sha256": "0" * 64}
    (b / "skill.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    assert integrity.calculate(a)["manifest_sha256"] == integrity.calculate(b)["manifest_sha256"]
    assert integrity.calculate(a)["package_sha256"] == integrity.calculate(b)["package_sha256"]


def test_package_hash_changes_when_skill_content_changes(tmp_path):
    skill = tmp_path / "skill"
    write_skill(skill)
    before = integrity.calculate(skill)["package_sha256"]
    (skill / "SKILL.md").write_text("---\nname: demo\n---\n# Changed\n", encoding="utf-8")
    after = integrity.calculate(skill)["package_sha256"]
    assert before != after


def test_new_resource_directory_is_automatically_covered(tmp_path):
    skill = tmp_path / "skill"
    write_skill(skill)
    before = integrity.calculate(skill)["package_sha256"]
    (skill / "resources").mkdir()
    (skill / "resources" / "policy.txt").write_text("governed", encoding="utf-8")
    after = integrity.calculate(skill)["package_sha256"]
    assert before != after


def test_generated_result_files_do_not_change_package_hash(tmp_path):
    skill = tmp_path / "skill"
    write_skill(skill)
    (skill / "evals").mkdir()
    before = integrity.calculate(skill)["package_sha256"]
    (skill / "evals" / "golden-results.json").write_text('{"verified": true}', encoding="utf-8")
    after = integrity.calculate(skill)["package_sha256"]
    assert before == after


def test_generated_regression_baseline_does_not_change_package_hash(tmp_path):
    skill = tmp_path / "skill"
    write_skill(skill)
    (skill / "evals").mkdir()
    before = integrity.calculate(skill)["package_sha256"]
    (skill / "evals" / "regression-baseline.json").write_text(
        '{"verified": true, "metrics": {"success": 1.0}}', encoding="utf-8"
    )
    after = integrity.calculate(skill)["package_sha256"]
    assert before == after


def test_evaluation_definition_still_changes_package_hash(tmp_path):
    skill = tmp_path / "skill"
    write_skill(skill)
    (skill / "evals").mkdir()
    before = integrity.calculate(skill)["package_sha256"]
    (skill / "evals" / "golden.yaml").write_text("schema_version: '1.0'\ntasks: []\n", encoding="utf-8")
    after = integrity.calculate(skill)["package_sha256"]
    assert before != after


def test_agenticos_export_matches_schema_for_canonical_skill():
    skill_dir = ROOT / "skills" / "services" / "zabbix-proxi-monitor"
    payload = agenticos_export.build_export(
        skill_dir,
        "sramiweb/skills-brain",
        "a" * 40,
    )
    schema = json.loads((ROOT / "schemas" / "agenticos-export.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(payload, schema)
    assert payload["contract_version"] == "1.1"
    assert payload["skill"]["id"] == "zabbix-proxy-monitor"
    assert payload["skill"]["contracts"] == {"inputs": [], "outputs": []}
    assert "connectors" not in payload
    assert "tenants" not in payload


def test_agenticos_export_preserves_typed_product_handoff_contract():
    skill_dir = ROOT / "skills" / "product" / "feature-specification"
    payload = agenticos_export.build_export(
        skill_dir,
        "sramiweb/skills-brain",
        "b" * 40,
    )
    schema = json.loads((ROOT / "schemas" / "agenticos-export.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(payload, schema)

    assert payload["contract_version"] == "1.1"
    assert payload["skill"]["id"] == "feature-specification"
    input_contract = payload["skill"]["contracts"]["inputs"][0]
    assert input_contract["schema_id"] == "product.discovery-result.v1"
    assert input_contract["source"] == "skill"
    assert input_contract["required"] is True
    assert input_contract["from_capabilities"] == ["product.discover"]
    assert input_contract["allowed_data_classes"] == ["S0", "S1", "S2"]
    assert payload["skill"]["contracts"]["outputs"][0]["schema_id"] == "product.feature-specification.v1"


def test_agenticos_export_rejects_floating_or_short_commit():
    skill_dir = ROOT / "skills" / "services" / "zabbix-proxi-monitor"
    try:
        agenticos_export.build_export(skill_dir, "sramiweb/skills-brain", "main")
    except ValueError as exc:
        assert "40-character" in str(exc)
    else:
        raise AssertionError("floating ref must be rejected")
