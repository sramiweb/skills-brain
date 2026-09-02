#!/usr/bin/env python3
"""Skills Brain validator.

Validates canonical skill packages without mutating the local environment.
Schema v2.0 is supported for migration only. New skills must use v2.1.
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
    import yaml
except ImportError as exc:
    print("Missing dependencies. Install with: pip install -r requirements-dev.txt", file=sys.stderr)
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "skills"
SCHEMAS = {
    "2.0": ROOT / "schemas" / "skill-v2.0.schema.json",
    "2.1": ROOT / "schemas" / "skill.schema.json",
}


def load_manifest(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("skill.yaml must contain a YAML object")
    return data


def load_schema(version: str):
    schema_path = SCHEMAS.get(version)
    if schema_path is None:
        raise ValueError(f"Unsupported schema_version: {version}")
    with schema_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_capability_ontology():
    path = ROOT / "standards" / "capabilities.yaml"
    if not path.exists():
        return {"capabilities": {}, "tool_capabilities": {}}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    schema_path = ROOT / "schemas" / "capability.schema.json"
    with schema_path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    jsonschema.validate(data, schema)
    return data


def validate_yaml(skill_yaml_path: Path):
    try:
        skill_data = load_manifest(skill_yaml_path)
        version = str(skill_data.get("schema_version", ""))
        schema = load_schema(version)
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(instance=skill_data, schema=schema)
        return True, "Valid"
    except (ValueError, json.JSONDecodeError) as exc:
        return False, str(exc)
    except jsonschema.ValidationError as exc:
        location = ".".join(str(part) for part in exc.absolute_path)
        prefix = f"{location}: " if location else ""
        return False, prefix + exc.message


def validate_frontmatter(skill_md_path: Path):
    required_fields = ["name", "description", "license", "compatibility", "metadata"]
    content = skill_md_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "Missing frontmatter delimiter (---)"
    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return False, "Missing closing frontmatter delimiter"
    frontmatter = yaml.safe_load(content[4:end_idx])
    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a YAML object"
    missing = [field for field in required_fields if field not in frontmatter]
    if missing:
        return False, f"Missing frontmatter fields: {missing}"
    return True, "Valid"


def validate_capabilities(manifest):
    if str(manifest.get("schema_version")) != "2.1":
        return []
    ontology = load_capability_ontology()
    issues = []
    known_skills = ontology.get("capabilities", {})
    known_tools = ontology.get("tool_capabilities", {})

    for capability in manifest.get("capabilities", []):
        entry = known_skills.get(capability)
        if entry is None:
            issues.append(f"Unknown capability '{capability}'")
        elif entry.get("status") == "deprecated":
            issues.append(f"Deprecated capability '{capability}' must not be introduced")

    for capability in manifest.get("requirements", {}).get("tool_capabilities", []):
        entry = known_tools.get(capability)
        if entry is None:
            issues.append(f"Unknown tool capability '{capability}'")
        elif entry.get("status") == "deprecated":
            issues.append(f"Deprecated tool capability '{capability}' must not be introduced")

    for contract in (manifest.get("contracts") or {}).get("inputs", []):
        for capability in contract.get("from_capabilities", []):
            entry = known_skills.get(capability)
            if entry is None:
                issues.append(
                    f"Unknown handoff source capability '{capability}' in input contract '{contract.get('id')}'"
                )
            elif entry.get("status") == "deprecated":
                issues.append(
                    f"Deprecated handoff source capability '{capability}' in input contract '{contract.get('id')}'"
                )

    return issues


def validate_contracts(manifest):
    if str(manifest.get("schema_version")) != "2.1":
        return []

    issues = []
    contracts = manifest.get("contracts") or {}
    inputs = contracts.get("inputs") or []
    outputs = contracts.get("outputs") or []

    input_ids = [str(item.get("id")) for item in inputs]
    output_ids = [str(item.get("id")) for item in outputs]
    if len(input_ids) != len(set(input_ids)):
        issues.append("Duplicate contracts.inputs id")
    if len(output_ids) != len(set(output_ids)):
        issues.append("Duplicate contracts.outputs id")

    skill_allowed_data = set((manifest.get("data_classes") or {}).get("allowed") or [])
    if skill_allowed_data:
        for output in outputs:
            data_class = output.get("data_class")
            if data_class not in skill_allowed_data:
                issues.append(
                    f"Output contract '{output.get('id')}' data_class '{data_class}' is outside skill data_classes.allowed"
                )

    return issues


def validate_skill(skill_path):
    skill_path = Path(skill_path)
    errors = []
    skill_md = skill_path / "SKILL.md"
    skill_yaml = skill_path / "skill.yaml"

    if not skill_md.exists():
        errors.append(f"Missing SKILL.md in {skill_path}")
    else:
        try:
            valid, message = validate_frontmatter(skill_md)
        except UnicodeDecodeError as exc:
            valid, message = False, f"Invalid UTF-8: {exc}"
        if not valid:
            errors.append(f"SKILL.md: {message}")

    if not skill_yaml.exists():
        errors.append(f"Missing skill.yaml in {skill_path}")
    else:
        try:
            valid, message = validate_yaml(skill_yaml)
        except UnicodeDecodeError as exc:
            valid, message = False, f"Invalid UTF-8: {exc}"
        if not valid:
            errors.append(f"skill.yaml: {message}")
        else:
            try:
                manifest = load_manifest(skill_yaml)
                errors.extend(validate_capabilities(manifest))
                errors.extend(validate_contracts(manifest))
            except Exception as exc:
                errors.append(f"Capability/contract validation failed: {exc}")

    return errors


def iter_skill_dirs():
    if not SKILLS_ROOT.exists():
        return []
    return sorted({path.parent for path in SKILLS_ROOT.rglob("skill.yaml")})


def validate_all():
    all_errors = {}
    seen_ids = {}
    seen_aliases = {}

    for skill_dir in iter_skill_dirs():
        errors = validate_skill(skill_dir)
        manifest_path = skill_dir / "skill.yaml"
        try:
            manifest = load_manifest(manifest_path)
            skill_id = manifest.get("id")
            if skill_id:
                if skill_id in seen_ids:
                    errors.append(f"Duplicate skill id '{skill_id}' also used by {seen_ids[skill_id]}")
                else:
                    seen_ids[skill_id] = str(skill_dir)
            for alias in manifest.get("aliases", []):
                if alias == skill_id:
                    errors.append(f"Alias '{alias}' duplicates canonical id")
                if alias in seen_aliases:
                    errors.append(f"Duplicate alias '{alias}' also used by {seen_aliases[alias]}")
                else:
                    seen_aliases[alias] = str(skill_dir)
        except Exception as exc:
            errors.append(f"Unable to inspect manifest identity: {exc}")
        if errors:
            all_errors[str(skill_dir)] = errors

    collisions = set(seen_ids).intersection(seen_aliases)
    for value in sorted(collisions):
        owner = seen_aliases[value]
        all_errors.setdefault(owner, []).append(f"Alias '{value}' collides with a canonical skill id")

    return all_errors


def validate_all_skills():
    return validate_all()


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--all":
        print("Validating all skills...")
        errors = validate_all()
        if errors:
            print(f"\nFound errors in {len(errors)} skill(s):\n")
            for skill, skill_errors in errors.items():
                print(f"  {skill}:")
                for error in skill_errors:
                    print(f"    - {error}")
            raise SystemExit(1)
        print("All skills are valid.")
        return

    skill_path = Path(sys.argv[1])
    errors = validate_skill(skill_path)
    if errors:
        print(f"Validation failed for {skill_path}:\n")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)
    print(f"{skill_path} is valid.")


if __name__ == "__main__":
    main()
