import json
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "skills" / "klerbot"

EXPECTED = {
    "klerbot-product-context": "klerbot.product.context",
    "klerbot-architecture": "klerbot.architecture",
    "klerbot-code-conventions": "klerbot.code.conventions",
    "klerbot-brand-voice": "klerbot.brand.voice",
}


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_klerbot_wave1_context_pack_is_schema_valid_and_read_only():
    skill_schema = _json(ROOT / "schemas" / "skill.schema.json")
    golden_schema = _json(ROOT / "schemas" / "golden.schema.json")

    for skill_id, capability in EXPECTED.items():
        skill_dir = PACK / skill_id
        manifest = _yaml(skill_dir / "skill.yaml")
        golden = _yaml(skill_dir / "evals" / "golden.yaml")

        jsonschema.validate(instance=manifest, schema=skill_schema)
        jsonschema.validate(instance=golden, schema=golden_schema)

        assert manifest["schema_version"] == "2.1"
        assert manifest["id"] == skill_id
        assert manifest["status"] == "candidate"
        assert manifest["capabilities"] == [capability]
        assert manifest["side_effects"] == "none"
        assert manifest["security"] == {
            "network": {"outbound": False},
            "filesystem": {"read": False, "write": False},
            "shell": False,
            "destructive_operations": False,
        }
        assert not (manifest.get("requirements") or {}).get("tool_capabilities")
        assert "https://github.com/sramiweb/wissql" in manifest["provenance"]["derived_from"]
        assert manifest["evaluation"]["golden_tasks"] == "required"
        assert len(golden["tasks"]) >= 3
        assert (skill_dir / "SKILL.md").exists()


def test_klerbot_pack_does_not_duplicate_generic_roadmap_method():
    assert not (PACK / "klerbot-roadmap-method").exists()

    readme = (PACK / "README.md").read_text(encoding="utf-8")
    assert "roadmap-prioritization" in readme
    assert "klerbot-product-context" in readme
    assert "unless Klerbot later develops a genuinely distinct" in readme
