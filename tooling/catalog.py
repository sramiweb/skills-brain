#!/usr/bin/env python3
"""
Skills Brain Catalog Generator v2

Gé««nè««re automatiquement le catalog des skills (index.json, capabilities.json, etc.)

Usage:
    python tooling/catalog.py
"""

import json
import os
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Installing: pip install pyyaml")
    os.system("pip install pyyaml")
    import yaml


def extract_capabilities(skill_path):
    """Extrait les capacités d'un skill depuis skill.yaml ou SKILL.md"""
    skill_yaml = skill_path / "skill.yaml"
    skill_md = skill_path / "SKILL.md"

    # Priorité«« à skill.yaml
    if skill_yaml.exists():
        with open(skill_yaml, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("capabilities", [])

    # Fallback: extraire depuis SKILL.md frontmatter
    if skill_md.exists():
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()

        if content.startswith("---"):
            end_idx = content.find("\n---", 3)
            if end_idx != -1:
                frontmatter = yaml.safe_load(content[4:end_idx])
                # Capabilit é s dé «duites de la caté««gorie
                category = frontmatter.get("metadata", {}).get("category", "unknown")
                return [f"{category}.skill"]

    return []


def extract_metadata(skill_path):
    """Extrait les mé «tadonn ées d'un skill"""
    skill_yaml = skill_path / "skill.yaml"
    skill_md = skill_path / "SKILL.md"

    metadata = {
        "version": "0.0.0",
        "status": "draft",
        "quality_score": 0.0,
        "risk_level": 0,
    }

    if skill_yaml.exists():
        with open(skill_yaml, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            metadata.update({
                "version": data.get("version", "0.0.0"),
                "status": data.get("status", "draft"),
                "risk_level": data.get("risk", {}).get("level", 0),
            })

    return metadata


def generate_catalog():
    """Gé««nè««re le catalog complet des skills"""
    skills_dir = Path(__file__).parent.parent / "skills"
    catalog_dir = Path(__file__).parent.parent / "catalog"

    # Cré «er catalog/
    catalog_dir.mkdir(exist_ok=True)

    index = {}
    capabilities_map = {}
    dependencies = {}

    for category in ["agenticos", "templates", "services"]:
        cat_dir = skills_dir / category
        if not cat_dir.exists():
            continue

        for skill_dir in cat_dir.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue

            skill_id = f"{category}/{skill_dir.name}"
            capabilities = extract_capabilities(skill_dir)
            metadata = extract_metadata(skill_dir)

            # Index
            index[skill_id] = {
                "version": metadata["version"],
                "status": metadata["status"],
                "quality_score": metadata["quality_score"],
                "risk_level": metadata["risk_level"],
                "capabilities": capabilities,
                "path": f"skills/{category}/{skill_dir.name}",
            }

            # Capabilities map
            for cap in capabilities:
                if cap not in capabilities_map:
                    capabilities_map[cap] = []
                capabilities_map[cap].append(skill_id)

            # Dependencies (à«« compl éter)
            dependencies[skill_id] = {
                "requires": [],
                "optional": [],
                "conflicts": [],
            }

    # Sauvegarder
    with open(catalog_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    with open(catalog_dir / "capabilities.json", "w", encoding="utf-8") as f:
        json.dump(capabilities_map, f, indent=2, ensure_ascii=False)

    with open(catalog_dir / "dependencies.json", "w", encoding="utf-8") as f:
        json.dump(dependencies, f, indent=2, ensure_ascii=False)

    print(f"✅ Catalog gé «né««ré«« : {len(index)} skills, {len(capabilities_map)} capabilities")
    print(f"   → {catalog_dir}/index.json")
    print(f"   → {catalog_dir}/capabilities.json")
    print(f"   → {catalog_dir}/dependencies.json")


if __name__ == "__main__":
    generate_catalog()
