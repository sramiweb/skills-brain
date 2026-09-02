import importlib.util
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module("skills_brain_validate_handoffs", ROOT / "tooling" / "validate.py")


def base_manifest():
    return {
        "schema_version": "2.1",
        "id": "handoff-test",
        "version": "1.0.0",
        "status": "candidate",
        "description": "Typed handoff validation fixture.",
        "capabilities": ["product.feature.specify"],
        "risk": {"level": 1},
        "side_effects": "none",
        "security": {
            "network": {"outbound": False},
            "filesystem": {"read": False, "write": False},
            "shell": False,
            "destructive_operations": False,
        },
        "evaluation": {"golden_tasks": "required", "minimum_score": 0.8},
        "ownership": {"maintainer": "sramiweb"},
        "provenance": {"origin": "skills-brain"},
    }


def test_skill_source_input_requires_from_capabilities():
    manifest = base_manifest()
    manifest["contracts"] = {
        "inputs": [{
            "id": "discovery-result",
            "schema_id": "product.discovery-result.v1",
            "source": "skill",
            "required": True,
            "allowed_data_classes": ["S2"],
        }]
    }
    schema = json.loads((ROOT / "schemas" / "skill.schema.json").read_text(encoding="utf-8"))

    try:
        jsonschema.validate(manifest, schema)
    except jsonschema.ValidationError:
        return
    raise AssertionError("source=skill input contract must declare from_capabilities")


def test_unknown_handoff_source_capability_is_rejected_by_ontology_validator():
    manifest = base_manifest()
    manifest["contracts"] = {
        "inputs": [{
            "id": "discovery-result",
            "schema_id": "product.discovery-result.v1",
            "source": "skill",
            "required": True,
            "from_capabilities": ["unknown.product.capability"],
            "allowed_data_classes": ["S2"],
        }]
    }

    issues = validator.validate_capabilities(manifest)

    assert any("Unknown handoff source capability" in issue for issue in issues)


def test_output_contract_must_fit_declared_skill_data_classes():
    manifest = base_manifest()
    manifest["data_classes"] = {"allowed": ["S0", "S1", "S2"]}
    manifest["contracts"] = {
        "outputs": [{
            "id": "result",
            "schema_id": "product.feature-specification.v1",
            "data_class": "S3",
        }]
    }

    issues = validator.validate_contracts(manifest)

    assert any("outside skill data_classes.allowed" in issue for issue in issues)
