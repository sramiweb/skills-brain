import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_v21_schema_is_valid_json_schema():
    schema = load_json(ROOT / "schemas" / "skill.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)


def test_v20_schema_is_valid_json_schema():
    schema = load_json(ROOT / "schemas" / "skill-v2.0.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)


def test_v20_manifest_is_accepted_by_compat_schema():
    """Compatibility coverage must use a v2.0 fixture, not a migrated live skill."""
    manifest = {
        "schema_version": "2.0",
        "id": "legacy/example-skill",
        "name": "Legacy Example Skill",
        "version": "1.0.0",
        "status": "active",
        "description": "Representative legacy v2.0 manifest",
        "category": "legacy",
        "capabilities": ["legacy.example"],
        "risk": {"level": 2},
        "side_effects": ["Generates a local report"],
        "security": {
            "data_class": "internal",
            "permissions": ["read:files"],
        },
        "provenance": {
            "author": "fixture",
            "created": "2026-09-01",
            "source": "compatibility-test",
        },
        "relationships": {"requires": [], "optional": []},
        "evaluation": {"quality_score": 0.0},
    }
    schema = load_json(ROOT / "schemas" / "skill-v2.0.schema.json")
    jsonschema.validate(instance=manifest, schema=schema)


def test_v21_rejects_unknown_top_level_property():
    schema = load_json(ROOT / "schemas" / "skill.schema.json")
    manifest = {
        "schema_version": "2.1",
        "id": "example-skill",
        "version": "1.0.0",
        "status": "draft",
        "description": "Example",
        "capabilities": ["example.run"],
        "risk": {"level": 0},
        "side_effects": "none",
        "security": {
            "network": {"outbound": False},
            "filesystem": {"read": True, "write": False},
            "shell": False,
            "destructive_operations": False,
        },
        "evaluation": {"golden_tasks": "optional", "minimum_score": 0.0},
        "ownership": {"maintainer": "skills-brain"},
        "provenance": {"origin": "skills-brain"},
        "typo_field": True,
    }
    try:
        jsonschema.validate(instance=manifest, schema=schema)
    except jsonschema.ValidationError:
        return
    raise AssertionError("v2.1 schema must reject unknown top-level properties")
