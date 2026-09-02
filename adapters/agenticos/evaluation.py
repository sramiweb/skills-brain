#!/usr/bin/env python3
"""AgenticOS adapter for Skills Brain runtime qualification.

This module does not call AgenticOS, models or tools. It translates a content-
addressed Skills Brain evaluation request into a runtime plan and converts a
runtime observation back into the canonical runner-results contract. It never
judges semantic correctness; independent verification remains mandatory.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas"


class AdapterError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AdapterError(f"{path}: expected JSON object")
    return data


def _schema(name: str) -> dict:
    return _json(SCHEMAS / name)


def _validate(data: dict, schema_name: str) -> None:
    validator = jsonschema.Draft202012Validator(
        _schema(schema_name), format_checker=jsonschema.FormatChecker()
    )
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    if errors:
        raise AdapterError(
            f"{schema_name}: " + "; ".join(error.message for error in errors[:8])
        )


def build_plan(
    request: dict,
    *,
    tenant: str,
    agent: str,
    data_class: str,
    model: str | None = None,
    context_max_bytes: int = 262144,
) -> dict:
    """Build a non-authorizing AgenticOS execution plan from an eval request."""
    _validate(request, "eval-run.schema.json")
    if data_class not in {"S0", "S1", "S2", "S3"}:
        raise AdapterError(f"unsupported data class: {data_class}")

    expected = {
        "id": request["skill"]["id"],
        "version": request["skill"]["version"],
        "package_sha256": request["skill"]["package_sha256"],
    }
    if request.get("source_commit"):
        expected["source_commit"] = request["source_commit"]

    jobs = []
    for item in request["items"]:
        if item["kind"] == "golden_task":
            mission = str((item.get("input") or {}).get("mission") or "")
        else:
            regression = item.get("input") or {}
            mission = (
                "Measure the declared regression check without judging it yourself. "
                f"Metric={regression.get('metric')}; baseline={regression.get('baseline')}; "
                f"baseline_value={regression.get('baseline_value', 'UNBOUND')}; "
                f"direction={regression.get('direction')}; allowed_delta={regression.get('allowed_delta')}."
            )

        prompt = (
            "You are executing a Skills Brain qualification item in AgenticOS.\n"
            f"Evaluation run: {request['run_id']}\n"
            f"Item: {item['id']} ({item['kind']})\n"
            f"Exact upstream Skill: {expected['id']}@{expected['version']}\n"
            f"Expected package SHA256: {expected['package_sha256']}\n\n"
            "The runtime must load the exact upstream Skill through its normal Skills Brain binding. "
            "A read-only snapshot of the installed Skill package may be supplied as evaluation context. "
            "Treat relative fixture paths as relative to that snapshot. Do not modify files, widen tools, "
            "use hidden network context, or score the evaluation criteria yourself.\n\n"
            "Return an evidence-rich task answer. Cite the concrete repository/fixture paths used, clearly "
            "separate observed facts from inference, and state unresolved evidence gaps.\n\n"
            f"Mission:\n{mission}"
        )
        jobs.append(
            {
                "id": item["id"],
                "kind": item["kind"],
                "prompt": prompt,
                "package_context": {
                    "mode": "installed_skill_package",
                    "read_only": True,
                    "include": ["SKILL.md", "skill.yaml", "fixtures/**"],
                    "max_bytes": context_max_bytes,
                },
                "expected_upstream": dict(expected),
            }
        )

    runtime = {
        "platform": "agenticos",
        "tenant": tenant,
        "agent": agent,
        "data_class": data_class,
    }
    if model:
        runtime["model"] = model

    plan = {
        "contract_version": "1.0",
        "run_id": request["run_id"],
        "gate": request["gate"],
        "authorization": "not_granted",
        "skill": dict(expected),
        "runtime": runtime,
        "jobs": jobs,
    }
    _validate(plan, "agenticos-eval-plan.schema.json")
    return plan


def collect_runner_results(request: dict, observation: dict) -> dict:
    """Convert AgenticOS observations to runner-results without semantic judgment."""
    _validate(request, "eval-run.schema.json")
    _validate(observation, "agenticos-eval-observation.schema.json")
    if observation["run_id"] != request["run_id"]:
        raise AdapterError("run_id mismatch between evaluation request and AgenticOS observation")

    expected_items = {item["id"]: item for item in request["items"]}
    actual_items = {item["id"]: item for item in observation["executions"]}
    if len(actual_items) != len(observation["executions"]):
        raise AdapterError("duplicate AgenticOS execution item id")
    if set(expected_items) != set(actual_items):
        raise AdapterError("AgenticOS execution ids do not exactly match evaluation request")

    expected_skill = request["skill"]
    expected_commit = request.get("source_commit")
    model_values = set()
    results = []
    for item_id in sorted(expected_items):
        execution = actual_items[item_id]
        upstream = execution["upstream_skill"]
        if upstream["id"] != expected_skill["id"]:
            raise AdapterError(f"{item_id}: upstream Skill id mismatch")
        if upstream["version"] != expected_skill["version"]:
            raise AdapterError(f"{item_id}: upstream Skill version mismatch")
        if upstream["package_sha256"] != expected_skill["package_sha256"]:
            raise AdapterError(f"{item_id}: upstream package hash mismatch")
        if expected_commit and upstream.get("source_commit") != expected_commit:
            raise AdapterError(f"{item_id}: upstream source commit mismatch")

        runtime_status = execution["status"]
        status = "completed" if runtime_status == "succeeded" else (
            "skipped" if runtime_status == "skipped" else "error"
        )
        model = execution.get("model_used")
        if model:
            model_values.add(model)

        evidence = list(execution.get("evidence_refs") or [])
        evidence.extend(
            [
                f"agenticos://execution/{execution['exec_id']}",
                f"skills-brain://{upstream['id']}@{upstream['version']}#sha256={upstream['package_sha256']}",
            ]
        )
        if upstream.get("source_commit"):
            evidence.append(f"git://sramiweb/skills-brain@{upstream['source_commit']}")

        result = {
            "id": item_id,
            "status": status,
            "artifact_refs": list(execution.get("artifact_refs") or []),
            "evidence": list(dict.fromkeys(evidence)),
        }
        if execution.get("output"):
            result["output_summary"] = execution["output"]
        if status == "error":
            result["error"] = execution.get("error") or f"AgenticOS status={runtime_status}"
        results.append(result)

    runner = {
        "schema_version": "1.0",
        "run_id": request["run_id"],
        "generated_by": observation["generated_by"],
        "generated_at": observation.get("generated_at") or _now(),
        "runtime": "agenticos",
        "results": results,
    }
    if len(model_values) == 1:
        runner["model"] = next(iter(model_values))
    elif model_values:
        runner["model"] = "mixed"
    _validate(runner, "eval-runner-results.schema.json")
    return runner


def _write(data: dict, path: Path | None) -> None:
    text = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def main() -> int:
    parser = argparse.ArgumentParser(description="Skills Brain AgenticOS evaluation adapter")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan")
    plan.add_argument("request", type=Path)
    plan.add_argument("--tenant", required=True)
    plan.add_argument("--agent", required=True)
    plan.add_argument("--data-class", required=True, choices=["S0", "S1", "S2", "S3"])
    plan.add_argument("--model")
    plan.add_argument("--context-max-bytes", type=int, default=262144)
    plan.add_argument("--output", type=Path)

    collect = sub.add_parser("collect")
    collect.add_argument("request", type=Path)
    collect.add_argument("observation", type=Path)
    collect.add_argument("--output", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "plan":
            payload = build_plan(
                _json(args.request), tenant=args.tenant, agent=args.agent,
                data_class=args.data_class, model=args.model,
                context_max_bytes=args.context_max_bytes,
            )
        else:
            payload = collect_runner_results(_json(args.request), _json(args.observation))
        _write(payload, args.output)
        return 0
    except (AdapterError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"agenticos-evaluation-adapter: {exc}", file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
