from pathlib import Path
import json

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_capability_ontology_schema():
    ontology = yaml.safe_load((ROOT / "standards" / "capabilities.yaml").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas" / "capability.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(ontology, schema)


def test_all_v21_manifest_capabilities_are_known():
    ontology = yaml.safe_load((ROOT / "standards" / "capabilities.yaml").read_text(encoding="utf-8"))
    known_skills = set(ontology["capabilities"])
    known_tools = set(ontology["tool_capabilities"])

    for manifest_path in (ROOT / "skills").rglob("skill.yaml"):
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        if str(manifest.get("schema_version")) != "2.1":
            continue
        assert set(manifest.get("capabilities", [])) <= known_skills, manifest_path
        assert set(manifest.get("requirements", {}).get("tool_capabilities", [])) <= known_tools, manifest_path


def test_legacy_aliases_are_unique():
    aliases = {}
    for manifest_path in (ROOT / "skills").rglob("skill.yaml"):
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        for alias in manifest.get("aliases", []):
            assert alias not in aliases, f"duplicate alias {alias}: {manifest_path} and {aliases[alias]}"
            aliases[alias] = manifest_path
