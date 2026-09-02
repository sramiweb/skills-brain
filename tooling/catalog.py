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
EVALUATION_REPORT = ROOT / "reports" / "evaluation.json"


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


def load_evaluation_results(path: Path = EVALUATION_REPORT):
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def build_catalog(skills_root: Path = SKILLS_ROOT, evaluation_results=None):
    evaluation_results = evaluation_results or {}
    index = {}
    capabilities_map = {}
    dependencies = {}
    compatibility = {}

    manifest_paths = sorted(skills_root.rglob("skill.yaml")) if skills_root.exists() else []
    for manifest_path in manifest_paths:
        manifest = load_manifest(manifest_path)
        skill_id = canonical_id(manifest, manifest_path)
        if skill_id in index:
            raise ValueError(f"Duplicate skill id: {skill_id}")

        risk = manifest.get("risk") or {}
        evaluation = manifest.get("evaluation") or {}
        measured = evaluation_results.get(skill_id) or {}
        relationships = manifest.get("relationships") or {}
        legacy_dependencies = manifest.get("dependencies") or {}
        capabilities = list(manifest.get("capabilities") or [])
        requirements = manifest.get("requirements") or {}
        rel_path = manifest_path.parent.relative_to(ROOT).as_posix() if manifest_path.is_relative_to(ROOT) else manifest_path.parent.relative_to(skills_root).as_posix()

        measured_score = measured.get("score")
        if measured_score is not None:
            measured_score = float(measured_score)

        index[skill_id] = {
            "aliases": list(manifest.get("aliases") or []),
            "version": manifest.get("version", "0.0.0"),
            "schema_version": manifest.get("schema_version"),
            "status": manifest.get("status", "draft"),
            "quality_score": measured_score,
            "evaluation": {
                "minimum_score": evaluation.get("minimum_score"),
                "golden_tasks": evaluation.get("golden_tasks"),
                "passed": measured.get("passed") if measured else None,
            },
            "risk_level": risk.get("level", 0),
            "side_effects": manifest.get("side_effects", "unknown"),
            "capabilities": capabilities,
            "requirements": {
                "tool_capabilities": list(requirements.get("tool_capabilities") or []),
                "skills": list(requirements.get("skills") or []),
            },
            "data_classes": manifest.get("data_classes", {}),
            "compatibility": manifest.get("compatibility", {}),
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

    return {
        "index.json": index,
        "capabilities.json": capabilities_map,
        "dependencies.json": dependencies,
        "compatibility.json": compatibility,
    }


def generate_catalog():
    CATALOG_ROOT.mkdir(exist_ok=True)
    outputs = build_catalog(evaluation_results=load_evaluation_results())

    for filename, payload in outputs.items():
        with (CATALOG_ROOT / filename).open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")

    index = outputs["index.json"]
    capabilities_map = outputs["capabilities.json"]
    print(f"Catalog generated: {len(index)} skills, {len(capabilities_map)} capabilities")


if __name__ == "__main__":
    generate_catalog()
