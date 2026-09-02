#!/usr/bin/env python3
"""Skills Brain capability resolver.

Resolution is advisory only. Eligibility filters run before ranking and never grant
runtime authorization. AgenticOS remains responsible for tenant/tool/policy checks.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "skills"
REQUEST_SCHEMA = ROOT / "schemas" / "resolution-request.schema.json"
ONTOLOGY_PATH = ROOT / "standards" / "capabilities.yaml"

STATUS_SCORE = {
    "draft": 0.20,
    "review": 0.40,
    "candidate": 0.65,
    "approved": 0.90,
    "active": 1.00,
    "deprecated": 0.10,
}

COMPARATOR_RE = re.compile(r"^(>=|<=|>|<|==|=)?\s*([0-9]+(?:\.[0-9]+){0,2})$")


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def parse_version(value: str) -> tuple[int, int, int]:
    parts = value.split(".")
    if not 1 <= len(parts) <= 3 or any(not part.isdigit() for part in parts):
        raise ValueError(f"Unsupported numeric version: {value}")
    numbers = [int(part) for part in parts]
    while len(numbers) < 3:
        numbers.append(0)
    return numbers[0], numbers[1], numbers[2]


def compatibility_satisfied(spec: str, version: str) -> bool:
    """Evaluate a deliberately small fail-closed numeric compatibility syntax.

    Supported examples: `>=3.1`, `>=3.1,<4`, `3.1`, `==3.1.2`.
    """

    actual = parse_version(version)
    clauses = [clause.strip() for clause in spec.split(",") if clause.strip()]
    if not clauses:
        return False

    for clause in clauses:
        match = COMPARATOR_RE.fullmatch(clause)
        if not match:
            return False
        operator = match.group(1) or "=="
        expected = parse_version(match.group(2))
        checks = {
            ">=": actual >= expected,
            "<=": actual <= expected,
            ">": actual > expected,
            "<": actual < expected,
            "==": actual == expected,
            "=": actual == expected,
        }
        if not checks[operator]:
            return False
    return True


def load_ontology() -> tuple[set[str], set[str]]:
    ontology = load_yaml(ONTOLOGY_PATH)
    capabilities = set((ontology.get("capabilities") or {}).keys())
    tool_capabilities = set((ontology.get("tool_capabilities") or {}).keys())
    return capabilities, tool_capabilities


def validate_request(request: dict) -> None:
    jsonschema.validate(request, load_json(REQUEST_SCHEMA))
    known_capabilities, known_tools = load_ontology()
    unknown_capabilities = sorted(set(request["capabilities"]) - known_capabilities)
    unknown_tools = sorted(set(request["available_tool_capabilities"]) - known_tools)
    if unknown_capabilities:
        raise ValueError("Unknown requested capabilities: " + ", ".join(unknown_capabilities))
    if unknown_tools:
        raise ValueError("Unknown available tool capabilities: " + ", ".join(unknown_tools))


def load_evaluation_report(request: dict) -> dict:
    configured = request.get("evaluation_report")
    if configured:
        path = Path(configured)
        if not path.is_absolute():
            path = ROOT / path
        return load_json(path)

    default = ROOT / "reports" / "evaluation.json"
    return load_json(default) if default.exists() else {}


def iter_manifests(skills_root: Path = SKILLS_ROOT):
    for path in sorted(skills_root.rglob("skill.yaml")):
        yield path, load_yaml(path)


def assess_candidate(manifest_path: Path, manifest: dict, request: dict, evaluation_report: dict) -> dict:
    requested = set(request["capabilities"])
    skill_capabilities = set(manifest.get("capabilities") or [])
    matched = sorted(requested & skill_capabilities)
    missing = sorted(requested - skill_capabilities)
    coverage = len(matched) / len(requested)

    reasons: list[str] = []
    status = str(manifest.get("status", "draft"))
    if status not in set(request["allowed_status"]):
        reasons.append(f"status_denied:{status}")
    if status == "quarantined":
        reasons.append("quarantined")
    if coverage == 0:
        reasons.append("no_capability_overlap")

    risk = int((manifest.get("risk") or {}).get("level", 4))
    if risk > int(request["max_risk"]):
        reasons.append(f"risk_exceeds_max:{risk}>{request['max_risk']}")

    requirements = manifest.get("requirements") or {}
    required_tools = set(requirements.get("tool_capabilities") or [])
    available_tools = set(request["available_tool_capabilities"])
    missing_tools = sorted(required_tools - available_tools)
    if missing_tools:
        reasons.append("missing_tools:" + ",".join(missing_tools))

    requested_data_class = request.get("data_class")
    if requested_data_class:
        allowed_data = set((manifest.get("data_classes") or {}).get("allowed") or [])
        if not allowed_data:
            if not request.get("allow_unspecified_data_class", False):
                reasons.append("data_class_unspecified")
        elif requested_data_class not in allowed_data:
            reasons.append(f"data_class_denied:{requested_data_class}")

    runtime = request.get("runtime")
    compatibility_note = None
    if runtime:
        runtime_name = runtime["name"]
        runtime_version = runtime["version"]
        compatibility = manifest.get("compatibility") or {}
        spec = compatibility.get(runtime_name)
        if spec is None:
            compatibility_note = "unspecified"
            if runtime.get("require_explicit_compatibility", False):
                reasons.append(f"compatibility_unspecified:{runtime_name}")
        else:
            try:
                if not compatibility_satisfied(str(spec), runtime_version):
                    reasons.append(f"runtime_incompatible:{runtime_name}:{runtime_version}:{spec}")
            except ValueError:
                reasons.append(f"runtime_compatibility_unparseable:{runtime_name}:{spec}")

    skill_id = str(manifest.get("id"))
    evaluation = evaluation_report.get(skill_id) or {}
    quality = float(evaluation.get("score", 0.0))
    risk_fitness = max(0.0, 1.0 - (risk / 4.0))
    lifecycle = STATUS_SCORE.get(status, 0.0)
    score = round((coverage * 0.55) + (quality * 0.25) + (lifecycle * 0.10) + (risk_fitness * 0.10), 4)

    try:
        rel_path = manifest_path.parent.relative_to(ROOT).as_posix()
    except ValueError:
        rel_path = str(manifest_path.parent)

    return {
        "id": skill_id,
        "version": manifest.get("version"),
        "status": status,
        "path": rel_path,
        "eligible": not reasons,
        "full_match": coverage == 1.0,
        "score": score if not reasons else None,
        "capability_coverage": round(coverage, 4),
        "matched_capabilities": matched,
        "missing_capabilities": missing,
        "required_tool_capabilities": sorted(required_tools),
        "missing_tool_capabilities": missing_tools,
        "risk_level": risk,
        "quality_score": quality,
        "compatibility": compatibility_note,
        "rejection_reasons": reasons,
    }


def resolve(request: dict, skills_root: Path = SKILLS_ROOT) -> dict:
    validate_request(request)
    evaluation_report = load_evaluation_report(request)

    assessed = [
        assess_candidate(path, manifest, request, evaluation_report)
        for path, manifest in iter_manifests(skills_root)
    ]
    eligible = [item for item in assessed if item["eligible"]]
    eligible.sort(
        key=lambda item: (
            bool(item["full_match"]),
            float(item["score"] or 0.0),
            float(item["quality_score"]),
            -int(item["risk_level"]),
            item["id"],
        ),
        reverse=True,
    )

    limit = int(request.get("limit", 10))
    result = {
        "resolver_version": "1.0",
        "authorization": "not_granted",
        "requested_capabilities": list(request["capabilities"]),
        "full_match_available": any(item["full_match"] for item in eligible),
        "candidates": eligible[:limit],
    }
    if request.get("include_rejected", False):
        result["rejected"] = [item for item in assessed if not item["eligible"]]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve Skills Brain capabilities to eligible Skill candidates")
    parser.add_argument("request", type=Path, help="Resolution request JSON")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    request = load_json(args.request)
    payload = resolve(request)
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
