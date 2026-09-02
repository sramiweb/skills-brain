import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


catalog = load_module("skills_brain_catalog", ROOT / "tooling" / "catalog.py")


def write_manifest(skills_root: Path):
    skill_dir = skills_root / "demo"
    skill_dir.mkdir(parents=True)
    manifest = {
        "schema_version": "2.1",
        "id": "demo-skill",
        "aliases": ["legacy/demo-skill"],
        "version": "1.0.0",
        "status": "candidate",
        "capabilities": ["engineering.code.review"],
        "requirements": {"tool_capabilities": ["filesystem.read"]},
        "contracts": {
            "inputs": [{
                "id": "review-context",
                "schema_id": "engineering.review-context.v1",
                "source": "skill",
                "required": True,
                "from_capabilities": ["engineering.codebase.analyze"],
                "allowed_data_classes": ["S1", "S2"],
            }],
            "outputs": [{
                "id": "review-result",
                "schema_id": "engineering.review-result.v1",
                "data_class": "S2",
            }],
        },
        "data_classes": {"allowed": ["S2"]},
        "risk": {"level": 1},
        "side_effects": "none",
        "evaluation": {"golden_tasks": "required", "minimum_score": 0.90},
        "compatibility": {"agenticos": ">=3.1"},
    }
    (skill_dir / "skill.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")


def test_catalog_uses_measured_score_not_minimum_threshold(tmp_path):
    skills_root = tmp_path / "skills"
    write_manifest(skills_root)

    outputs = catalog.build_catalog(
        skills_root=skills_root,
        evaluation_results={"demo-skill": {"score": 0.72, "passed": False}},
    )
    item = outputs["index.json"]["demo-skill"]

    assert item["quality_score"] == 0.72
    assert item["evaluation"]["minimum_score"] == 0.90
    assert item["evaluation"]["passed"] is False
    assert item["requirements"]["tool_capabilities"] == ["filesystem.read"]
    assert item["data_classes"]["allowed"] == ["S2"]
    assert item["contracts"]["inputs"][0]["schema_id"] == "engineering.review-context.v1"
    assert item["contracts"]["outputs"][0]["schema_id"] == "engineering.review-result.v1"
    assert item["contracts"]["outputs"][0]["data_class"] == "S2"


def test_catalog_without_evidence_uses_null_quality(tmp_path):
    skills_root = tmp_path / "skills"
    write_manifest(skills_root)

    outputs = catalog.build_catalog(skills_root=skills_root, evaluation_results={})
    item = outputs["index.json"]["demo-skill"]

    assert item["quality_score"] is None
    assert item["evaluation"]["minimum_score"] == 0.90
    assert item["evaluation"]["passed"] is None


def test_real_product_typed_handoff_contracts_are_catalogued():
    outputs = catalog.build_catalog(skills_root=ROOT / "skills", evaluation_results={})
    discovery = outputs["index.json"]["product-discovery"]
    specification = outputs["index.json"]["feature-specification"]

    assert discovery["contracts"]["outputs"] == [{
        "id": "discovery-result",
        "schema_id": "product.discovery-result.v1",
        "data_class": "S2",
        "description": "Evidence-backed product problems, opportunity hypotheses and unresolved discovery questions.",
    }]
    input_contract = specification["contracts"]["inputs"][0]
    assert input_contract["schema_id"] == "product.discovery-result.v1"
    assert input_contract["from_capabilities"] == ["product.discover"]
    assert input_contract["allowed_data_classes"] == ["S0", "S1", "S2"]
