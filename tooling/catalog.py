#!/usr/bin/env python3
"""Generate the Skills Brain catalog from canonical skill.yaml manifests."""

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    print("Missing dependency PyYAML. Install with: pip install -r requirements-dev.txt", file=sys.stderr)
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "skills"
CATALOG_ROOT = ROOT / "catalog"


def load_manifest(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def canonical_id(manifest, manifest_path: Path):
    skill_id = manifest.get("id")
    if not skill_id:
        raise ValueError(f"Missing id in {manifest_path}")
    return str(skill_id)


def generate_catalog():
    CATALOG_ROOT.mkdir(exist_ok=True)

    index = {}
    capabilities_map = {}
    dependencies = {}
    compatibility = {}

    manifest_paths = sorted(SKILLS_ROOT.rglob("skill.yaml")) if SKILLS_ROOT.exists() else []
    for manifest_path in manifest_paths:
        manifest = load_manifest(manifest_path)
        skill_id = canonical_id(manifest, manifest_path)
        if skill_id in index:
            raise ValueError(f"Duplicate skill id: {skill_id}")

        risk = manifest.get("risk") or {}
        evaluation = manifest.get("evaluation") or {}
        relationships = manifest.get("relationships") or {}
        legacy_dependencies = manifest.get("dependencies") or {}
        capabilities = list(manifest.get("capabilities") or [])
        rel_path = manifest_path.parent.relative_to(ROOT).as_posix()

        quality_score = evaluation.get("quality_score")
        if quality_score is None:
            quality_score = evaluation.get("minimum_score", 0.0)

        index[skill_id] = {
            "version": manifest.get("version", "0.0.0"),
            "schema_version": manifest.get("schema_version"),
            "status": manifest.get("status", "draft"),
            "quality_score": quality_score or 0.0,
            "risk_level": risk.get("level", 0),
            "side_effects": manifest.get("side_effects", "unknown"),
            "capabilities": capabilities,
            "path": rel_path,
        }

        for capability in capabilities:
            capabilities_map.setdefault(capability, []).append(skill_id)

        dependencies[skill_id] = {
            "requires": relationships.get("requires", legacy_dependencies.get("skills", [])),
            "optional": relationships.get("optional", []),
            "conflicts": relationships.get("conflicts", manifest.get("conflicts", [])),
            "extends": relationships.get("extends", []),
            "supersedes": relationships.get("supersedes", manifest.get("supersedes", [])),
            "composes": relationships.get("composes", []),
        }

        compatibility[skill_id] = manifest.get("compatibility", {})

    for capability in capabilities_map:
        capabilities_map[capability].sort()

    outputs = {
        "index.json": index,
        "capabilities.json": capabilities_map,
        "dependencies.json": dependencies,
        "compatibility.json": compatibility,
    }
    for filename, payload in outputs.items():
        with (CATALOG_ROOT / filename).open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")

    print(f"Catalog generated: {len(index)} skills, {len(capabilities_map)} capabilities")


if __name__ == "__main__":
    generate_catalog()
