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

    return errors


def iter_skill_dirs():
    if not SKILLS_ROOT.exists():
        return []
    return sorted({path.parent for path in SKILLS_ROOT.rglob("skill.yaml")})


def validate_all():
    all_errors = {}
    seen_ids = {}

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
        except Exception as exc:
            errors.append(f"Unable to inspect manifest identity: {exc}")
        if errors:
            all_errors[str(skill_dir)] = errors

    return all_errors


def validate_all_skills():
    """Stable API used by tooling/cli.py."""
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
