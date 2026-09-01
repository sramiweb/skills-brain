#!/usr/bin/env python3
"""
Skills Brain Validator v2

Validates SKILL.md and skill.yaml files against the v2 specification.

Usage:
    python tooling/validate.py <skill-path>
    python tooling/validate.py --all
"""

import json
import os
import sys
from pathlib import Path

try:
    import jsonschema
    import yaml
except ImportError:
    print("Installing dependencies: pip install jsonschema pyyaml")
    os.system("pip install jsonschema pyyaml")
    import jsonschema
    import yaml


def load_schema():
    """Load the skill schema from schemas/skill.schema.json"""
    schema_path = Path(__file__).parent.parent / "schemas" / "skill.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_yaml(skill_yaml_path, schema):
    """Validate a skill.yaml file against the schema"""
    with open(skill_yaml_path, "r", encoding="utf-8") as f:
        skill_data = yaml.safe_load(f)

    try:
        jsonschema.validate(instance=skill_data, schema=schema)
        return True, "Valid"
    except jsonschema.ValidationError as e:
        return False, str(e.message)


def validate_frontmatter(skill_md_path):
    """Validate SKILL.md frontmatter"""
    required_fields = ["name", "description", "license", "compatibility", "metadata"]

    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract frontmatter
    if not content.startswith("---"):
        return False, "Missing frontmatter delimiter (---)"

    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return False, "Missing closing frontmatter delimiter"

    frontmatter_yaml = content[4:end_idx]
    frontmatter = yaml.safe_load(frontmatter_yaml)

    missing = [f for f in required_fields if f not in frontmatter]
    if missing:
        return False, f"Missing frontmatter fields: {missing}"

    return True, "Valid"


def validate_skill(skill_path):
    """Validate a complete skill directory"""
    skill_path = Path(skill_path)
    errors = []

    # Check required files
    skill_md = skill_path / "SKILL.md"
    skill_yaml = skill_path / "skill.yaml"

    if not skill_md.exists():
        errors.append(f"Missing SKILL.md in {skill_path}")
    else:
        valid, msg = validate_frontmatter(skill_md)
        if not valid:
            errors.append(f"SKILL.md: {msg}")

    if not skill_yaml.exists():
        errors.append(f"Missing skill.yaml in {skill_path} (required for v2)")
    else:
        schema = load_schema()
        valid, msg = validate_yaml(skill_yaml, schema)
        if not valid:
            errors.append(f"skill.yaml: {msg}")

    # Check structure
    tests_dir = skill_path / "tests"
    evals_dir = skill_path / "evals"

    if not tests_dir.exists():
        errors.append(f"Missing tests/ directory (recommended)")

    if not evals_dir.exists():
        errors.append(f"Missing evals/ directory (recommended)")

    return errors


def validate_all():
    """Validate all skills in the repository"""
    skills_dir = Path(__file__).parent.parent / "skills"
    all_errors = {}

    for category in ["agenticos", "templates", "services"]:
        cat_dir = skills_dir / category
        if not cat_dir.exists():
            continue

        for skill_dir in cat_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith("."):
                errors = validate_skill(skill_dir)
                if errors:
                    all_errors[str(skill_dir)] = errors

    return all_errors


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--all":
        print("Validating all skills...")
        errors = validate_all()

        if errors:
            print(f"\n❌ Found errors in {len(errors)} skill(s):\n")
            for skill, errs in errors.items():
                print(f"  {skill}:")
                for err in errs:
                    print(f"    - {err}")
            sys.exit(1)
        else:
            print("✅ All skills are valid!")
            sys.exit(0)

    skill_path = sys.argv[1]
    errors = validate_skill(skill_path)

    if errors:
        print(f"❌ Validation failed for {skill_path}:\n")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(f"✅ {skill_path} is valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
