#!/usr/bin/env python3
"""Governed multi-Skill composition for Skills Brain.

The composer is advisory only. It selects the smallest eligible Skill set that
covers requested capabilities, closes declared dependencies, rejects conflicts,
and returns authorization=not_granted. Runtime permissions remain the consuming
runtime's responsibility.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from statistics import mean

import jsonschema
import yaml

TOOLING_DIR = Path(__file__).resolve().parent
if str(TOOLING_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLING_DIR))

import resolver  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "skills"
REQUEST_SCHEMA = ROOT / "schemas" / "composition-request.schema.json"
RESULT_SCHEMA = ROOT / "schemas" / "composition-result.schema.json"

SIDE_EFFECT_SCORE = {
    "none": 0,
    "local": 1,
    "reversible": 2,
    "external": 3,
    "destructive": 4,
    "unknown": 5,
}


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def resolver_request(request: dict, capabilities: list[str] | None = None) -> dict:
    keys = {
        "schema_version",
        "available_tool_capabilities",
        "allowed_status",
        "max_risk",
        "data_class",
        "allow_unspecified_data_class",
        "runtime",
        "evaluation_report",
    }
    payload = {key: request[key] for key in keys if key in request}
    payload["capabilities"] = list(capabilities or request["capabilities"])
    payload["limit"] = 50
    payload["include_rejected"] = True
    return payload


def validate_request(request: dict) -> None:
    jsonschema.validate(request, load_json(REQUEST_SCHEMA))
    # Reuse the resolver's ontology and runtime/tool/data-class validation.
    resolver.validate_request(resolver_request(request))


def load_manifests(skills_root: Path) -> dict[str, tuple[Path, dict]]:
    manifests: dict[str, tuple[Path, dict]] = {}
    for path in sorted(skills_root.rglob("skill.yaml")):
        manifest = load_yaml(path)
        skill_id = str(manifest.get("id") or "")
        if not skill_id:
            raise ValueError(f"Missing id in {path}")
        if skill_id in manifests:
            raise ValueError(f"Duplicate skill id: {skill_id}")
        manifests[skill_id] = (path, manifest)
    return manifests


def dependency_ids(manifest: dict) -> list[str]:
    requirements = manifest.get("requirements") or {}
    relationships = manifest.get("relationships") or {}
    values = list(requirements.get("skills") or []) + list(relationships.get("requires") or [])
    return sorted(set(str(value) for value in values))


def superseded_ids(manifest: dict) -> set[str]:
    return set(str(value) for value in ((manifest.get("relationships") or {}).get("supersedes") or []))


def assess(
    manifest_path: Path,
    manifest: dict,
    request: dict,
    evaluation_report: dict,
    capabilities: list[str] | None = None,
) -> dict:
    local_request = resolver_request(request, capabilities=capabilities)
    return resolver.assess_candidate(manifest_path, manifest, local_request, evaluation_report)


def dependency_closure(
    seed_ids: set[str],
    manifests: dict[str, tuple[Path, dict]],
    request: dict,
    evaluation_report: dict,
) -> tuple[set[str], list[str]]:
    closure = set(seed_ids)
    visiting: set[str] = set()
    visited: set[str] = set()
    reasons: list[str] = []

    def visit(skill_id: str, trail: list[str]) -> None:
        if skill_id in visited:
            return
        if skill_id in visiting:
            cycle = "->".join(trail + [skill_id])
            reasons.append(f"dependency_cycle:{cycle}")
            return
        if skill_id not in manifests:
            reasons.append(f"missing_dependency:{skill_id}")
            return

        visiting.add(skill_id)
        _, manifest = manifests[skill_id]
        for dependency_id in dependency_ids(manifest):
            if dependency_id not in manifests:
                reasons.append(f"missing_dependency:{skill_id}->{dependency_id}")
                continue

            dependency_path, dependency_manifest = manifests[dependency_id]
            dependency_caps = list(dependency_manifest.get("capabilities") or [])
            candidate = assess(
                dependency_path,
                dependency_manifest,
                request,
                evaluation_report,
                capabilities=dependency_caps,
            )
            if not candidate["eligible"]:
                detail = ",".join(candidate["rejection_reasons"])
                reasons.append(f"dependency_ineligible:{skill_id}->{dependency_id}:{detail}")
                continue

            closure.add(dependency_id)
            visit(dependency_id, trail + [skill_id])

        visiting.remove(skill_id)
        visited.add(skill_id)

    for seed_id in sorted(seed_ids):
        visit(seed_id, [])

    return closure, sorted(set(reasons))


def relationship_blockers(selected_ids: set[str], manifests: dict[str, tuple[Path, dict]]) -> list[str]:
    blockers: set[str] = set()
    for skill_id in sorted(selected_ids):
        _, manifest = manifests[skill_id]
        relationships = manifest.get("relationships") or {}
        for conflict in relationships.get("conflicts") or []:
            conflict_id = str(conflict)
            if conflict_id in selected_ids:
                pair = sorted([skill_id, conflict_id])
                blockers.add(f"conflict:{pair[0]}:{pair[1]}")
        for superseded in superseded_ids(manifest):
            if superseded in selected_ids:
                blockers.add(f"superseded_pair:{skill_id}:{superseded}")
    return sorted(blockers)


def topological_order(selected_ids: set[str], manifests: dict[str, tuple[Path, dict]]) -> tuple[list[str], list[str]]:
    order: list[str] = []
    state: dict[str, int] = {}
    blockers: list[str] = []

    def visit(skill_id: str, trail: list[str]) -> None:
        current = state.get(skill_id, 0)
        if current == 2:
            return
        if current == 1:
            blockers.append(f"dependency_cycle:{'->'.join(trail + [skill_id])}")
            return
        state[skill_id] = 1
        _, manifest = manifests[skill_id]
        for dependency_id in dependency_ids(manifest):
            if dependency_id in selected_ids:
                visit(dependency_id, trail + [skill_id])
        state[skill_id] = 2
        if skill_id not in order:
            order.append(skill_id)

    for skill_id in sorted(selected_ids):
        visit(skill_id, [])
    return order, sorted(set(blockers))


def side_effects_for(selected_ids: set[str], manifests: dict[str, tuple[Path, dict]]) -> str:
    effects = [str(manifests[skill_id][1].get("side_effects", "unknown")) for skill_id in selected_ids]
    return max(effects, key=lambda value: SIDE_EFFECT_SCORE.get(value, SIDE_EFFECT_SCORE["unknown"]), default="none")


def selected_skill_payload(
    skill_id: str,
    manifest: dict,
    dependency: bool,
) -> dict:
    requirements = manifest.get("requirements") or {}
    return {
        "id": skill_id,
        "version": manifest.get("version"),
        "risk_level": int((manifest.get("risk") or {}).get("level", 4)),
        "side_effects": str(manifest.get("side_effects", "unknown")),
        "required_tool_capabilities": sorted(set(requirements.get("tool_capabilities") or [])),
        "dependency": dependency,
    }


def build_result(
    request: dict,
    manifests: dict[str, tuple[Path, dict]],
    selected_ids: set[str],
    seed_ids: set[str],
    scores: dict[str, float],
    blockers: list[str],
    missing_capabilities: list[str],
    rejected: list[dict] | None = None,
) -> dict:
    requested = list(request["capabilities"])
    execution_order, topo_blockers = topological_order(selected_ids, manifests) if selected_ids else ([], [])
    blockers = sorted(set(blockers + topo_blockers))

    coverage = {}
    for capability in requested:
        providers = sorted(
            skill_id
            for skill_id in selected_ids
            if capability in set(manifests[skill_id][1].get("capabilities") or [])
        )
        owner = None
        if providers:
            owner = sorted(providers, key=lambda skill_id: (-scores.get(skill_id, 0.0), skill_id))[0]
        coverage[capability] = {"owner": owner, "providers": providers}

    combined_tools = sorted({
        tool
        for skill_id in selected_ids
        for tool in ((manifests[skill_id][1].get("requirements") or {}).get("tool_capabilities") or [])
    })
    composite_risk = max(
        [int((manifests[skill_id][1].get("risk") or {}).get("level", 4)) for skill_id in selected_ids],
        default=0,
    )

    payload = {
        "composer_version": "1.0",
        "authorization": "not_granted",
        "requested_capabilities": requested,
        "status": "composed" if selected_ids and not blockers and not missing_capabilities else "unresolved",
        "missing_capabilities": sorted(set(missing_capabilities)),
        "selected_skills": [
            selected_skill_payload(skill_id, manifests[skill_id][1], dependency=(skill_id not in seed_ids))
            for skill_id in execution_order
        ],
        "execution_order": execution_order,
        "coverage": coverage,
        "combined_requirements": {"tool_capabilities": combined_tools},
        "composite_risk": composite_risk,
        "composite_side_effects": side_effects_for(selected_ids, manifests),
        "blocking_reasons": blockers,
    }
    if request.get("include_rejected", False):
        payload["rejected_candidates"] = rejected or []

    jsonschema.validate(payload, load_json(RESULT_SCHEMA))
    return payload


def compose(request: dict, skills_root: Path = SKILLS_ROOT) -> dict:
    validate_request(request)
    manifests = load_manifests(skills_root)
    evaluation_report = resolver.load_evaluation_report(request)

    assessed = [
        assess(path, manifest, request, evaluation_report)
        for path, manifest in manifests.values()
    ]
    primary = [item for item in assessed if item["eligible"] and item["matched_capabilities"]]
    requested = set(request["capabilities"])
    max_skills = int(request.get("max_skills", 6))

    # Scores used only after eligibility, never to bypass a rejection.
    own_scores: dict[str, float] = {}
    for skill_id, (path, manifest) in manifests.items():
        own_caps = list(manifest.get("capabilities") or [])
        own = assess(path, manifest, request, evaluation_report, capabilities=own_caps)
        own_scores[skill_id] = float(own.get("score") or 0.0) if own["eligible"] else 0.0

    candidates_by_id = {item["id"]: item for item in primary}
    eligible_union = {
        capability
        for item in primary
        for capability in item["matched_capabilities"]
    }
    missing_from_eligible = sorted(requested - eligible_union)
    rejected = [item for item in assessed if not item["eligible"]]

    if missing_from_eligible:
        return build_result(
            request,
            manifests,
            selected_ids=set(),
            seed_ids=set(),
            scores=own_scores,
            blockers=["insufficient_eligible_capability_coverage"],
            missing_capabilities=missing_from_eligible,
            rejected=rejected,
        )

    ids = sorted(candidates_by_id)
    valid_options: list[tuple[tuple, set[str], set[str]]] = []
    invalid_blockers: set[str] = set()

    for size in range(1, min(len(ids), max_skills) + 1):
        for combo in itertools.combinations(ids, size):
            seed_ids = set(combo)
            covered = {
                capability
                for skill_id in seed_ids
                for capability in candidates_by_id[skill_id]["matched_capabilities"]
            }
            if not requested.issubset(covered):
                continue

            closure, dependency_blockers = dependency_closure(
                seed_ids, manifests, request, evaluation_report
            )
            blockers = list(dependency_blockers)
            if len(closure) > max_skills:
                blockers.append(f"max_skills_exceeded:{len(closure)}>{max_skills}")
            blockers.extend(relationship_blockers(closure, manifests))
            _, topo_blockers = topological_order(closure, manifests)
            blockers.extend(topo_blockers)
            blockers = sorted(set(blockers))
            if blockers:
                invalid_blockers.update(blockers)
                continue

            avg_score = mean(own_scores.get(skill_id, 0.0) for skill_id in closure)
            risk = max(int((manifests[skill_id][1].get("risk") or {}).get("level", 4)) for skill_id in closure)
            key = (len(closure), -avg_score, risk, tuple(sorted(closure)))
            valid_options.append((key, closure, seed_ids))

        if valid_options:
            # No larger base combination can beat a smaller sufficient composition.
            break

    if not valid_options:
        return build_result(
            request,
            manifests,
            selected_ids=set(),
            seed_ids=set(),
            scores=own_scores,
            blockers=sorted(invalid_blockers) or ["no_valid_composition"],
            missing_capabilities=[],
            rejected=rejected,
        )

    _, selected_ids, seed_ids = min(valid_options, key=lambda item: item[0])
    return build_result(
        request,
        manifests,
        selected_ids=selected_ids,
        seed_ids=seed_ids,
        scores=own_scores,
        blockers=[],
        missing_capabilities=[],
        rejected=rejected,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Compose eligible Skills into a governed capability plan")
    parser.add_argument("request", type=Path, help="Composition request JSON")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = compose(load_json(args.request))
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
