#!/usr/bin/env python3
"""Prepare and finalize Skills Brain Q4/Q5 evaluation runs.

The harness does not execute LLMs and does not judge its own outputs. It creates a
content-addressed run request, accepts observations from an external runner and
requires an independent verification artifact before producing the canonical
*-results.json consumed by tooling/evaluator.py.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
TOOLING = ROOT / "tooling"
if str(TOOLING) not in sys.path:
    sys.path.insert(0, str(TOOLING))

from integrity import calculate  # noqa: E402


class HarnessError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise HarnessError(f"{path}: expected JSON object")
    return data


def _yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise HarnessError(f"{path}: expected YAML object")
    return data


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _schema(name: str) -> dict:
    return _json(ROOT / "schemas" / name)


def _validate(data: dict, schema_name: str) -> None:
    validator = jsonschema.Draft202012Validator(
        _schema(schema_name), format_checker=jsonschema.FormatChecker()
    )
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    if errors:
        rendered = "; ".join(error.message for error in errors[:8])
        raise HarnessError(f"{schema_name}: {rendered}")


def _source_commit() -> str | None:
    try:
        value = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    if len(value) == 40 and all(char in "0123456789abcdef" for char in value.lower()):
        return value.lower()
    return None


def _relative_or_absolute(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _definition_for_gate(skill_dir: Path, gate: str) -> tuple[Path, dict, list[dict]]:
    if gate == "Q4":
        path = skill_dir / "evals" / "golden.yaml"
        if not path.exists():
            raise HarnessError(f"missing Golden Task definition: {path}")
        data = _yaml(path)
        _validate(data, "golden.schema.json")
        items = [
            {
                "id": task["id"],
                "kind": "golden_task",
                "input": {"mission": task["mission"], "expected": task["expected"]},
                "checks": list(task["criteria"]),
                "forbidden": list(task.get("forbidden") or []),
            }
            for task in data["tasks"]
        ]
        return path, data, items

    if gate == "Q5":
        path = skill_dir / "evals" / "regression.yaml"
        if not path.exists():
            raise HarnessError(f"missing regression definition: {path}")
        data = _yaml(path)
        _validate(data, "regression.schema.json")
        items = []
        for check in data["checks"]:
            items.append(
                {
                    "id": check["id"],
                    "kind": "regression_check",
                    "input": {
                        "baseline": data["baseline"],
                        "metric": check["metric"],
                        "allowed_delta": check["allowed_delta"],
                        "direction": check.get("direction", "no-change"),
                    },
                    "checks": [
                        "Observed result satisfies the declared baseline, metric, direction and allowed_delta policy."
                    ],
                    "forbidden": [],
                }
            )
        return path, data, items

    raise HarnessError(f"unsupported gate: {gate}; expected Q4 or Q5")


def prepare_run(
    skill_dir: Path,
    gate: str,
    *,
    run_id: str | None = None,
    output_dir: Path | None = None,
) -> Path:
    skill_dir = skill_dir.resolve()
    manifest = _yaml(skill_dir / "skill.yaml")
    gate = gate.upper()
    definition_path, _, items = _definition_for_gate(skill_dir, gate)
    hashes = calculate(skill_dir)
    request = {
        "schema_version": "1.0",
        "run_id": run_id or f"{manifest['id']}-{gate.lower()}-{uuid.uuid4().hex[:12]}",
        "gate": gate,
        "skill": {
            "id": manifest["id"],
            "version": str(manifest["version"]),
            "package_sha256": hashes["package_sha256"],
        },
        "definition": {
            "path": _relative_or_absolute(definition_path),
            "sha256": _sha256(definition_path),
        },
        "generated_at": _now(),
        "items": items,
    }
    commit = _source_commit()
    if commit:
        request["source_commit"] = commit
    _validate(request, "eval-run.schema.json")

    if output_dir is None:
        output_dir = ROOT / "reports" / "eval-runs" / manifest["id"] / request["run_id"]
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "request.json"
    target.write_text(json.dumps(request, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return target


def _unique_by_id(items: list[dict], label: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for item in items:
        item_id = item.get("id")
        if item_id in out:
            raise HarnessError(f"duplicate {label} id: {item_id}")
        out[item_id] = item
    return out


def _require_exact_ids(expected: set[str], actual: set[str], label: str) -> None:
    if expected != actual:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise HarnessError(f"{label} ids mismatch; missing={missing}, extra={extra}")


def _check_verification_coverage(request_item: dict, verification_item: dict) -> None:
    expected_checks = list(request_item["checks"])
    actual_checks = [entry["criterion"] for entry in verification_item["criteria_checks"]]
    if len(actual_checks) != len(set(actual_checks)):
        raise HarnessError(f"duplicate criterion verification: {request_item['id']}")
    if set(actual_checks) != set(expected_checks):
        raise HarnessError(f"criterion coverage mismatch: {request_item['id']}")

    expected_forbidden = list(request_item.get("forbidden") or [])
    actual_forbidden = [entry["rule"] for entry in verification_item["forbidden_checks"]]
    if len(actual_forbidden) != len(set(actual_forbidden)):
        raise HarnessError(f"duplicate forbidden verification: {request_item['id']}")
    if set(actual_forbidden) != set(expected_forbidden):
        raise HarnessError(f"forbidden-rule coverage mismatch: {request_item['id']}")


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def finalize_run(
    skill_dir: Path,
    request_path: Path,
    runner_results_path: Path,
    verification_path: Path,
    *,
    output_path: Path | None = None,
) -> Path:
    skill_dir = skill_dir.resolve()
    request = _json(request_path)
    runner = _json(runner_results_path)
    verification = _json(verification_path)
    _validate(request, "eval-run.schema.json")
    _validate(runner, "eval-runner-results.schema.json")
    _validate(verification, "eval-verification.schema.json")

    if runner["run_id"] != request["run_id"] or verification["run_id"] != request["run_id"]:
        raise HarnessError("run_id mismatch between request, runner results and verification")
    if verification["independent"] is not True:
        raise HarnessError("verification must be independent before Q4/Q5 evidence can be finalized")
    if verification["verified_by"] == runner["generated_by"]:
        raise HarnessError("runner and verifier identities must differ")

    manifest = _yaml(skill_dir / "skill.yaml")
    if manifest["id"] != request["skill"]["id"] or str(manifest["version"]) != request["skill"]["version"]:
        raise HarnessError("skill identity/version changed since evaluation request")
    current_hash = calculate(skill_dir)["package_sha256"]
    if current_hash != request["skill"]["package_sha256"]:
        raise HarnessError("skill package changed since evaluation request; prepare a new run")

    definition_path = skill_dir / "evals" / ("golden.yaml" if request["gate"] == "Q4" else "regression.yaml")
    if not definition_path.exists() or _sha256(definition_path) != request["definition"]["sha256"]:
        raise HarnessError("evaluation definition changed since run preparation")

    request_items = _unique_by_id(request["items"], "request")
    runner_items = _unique_by_id(runner["results"], "runner")
    verification_items = _unique_by_id(verification["results"], "verification")
    ids = set(request_items)
    _require_exact_ids(ids, set(runner_items), "runner")
    _require_exact_ids(ids, set(verification_items), "verification")

    results = []
    for item_id in sorted(ids):
        requested = request_items[item_id]
        observed = runner_items[item_id]
        checked = verification_items[item_id]
        _check_verification_coverage(requested, checked)

        checks = checked["criteria_checks"]
        forbidden = checked["forbidden_checks"]
        expected_ok = checked["expected_match"]["passed"] is True
        criteria_ok = all(entry["passed"] is True for entry in checks)
        forbidden_ok = all(entry["triggered"] is False for entry in forbidden)
        execution_ok = observed["status"] == "completed"

        total = 1 + len(checks) + len(forbidden)
        passed_count = int(expected_ok)
        passed_count += sum(1 for entry in checks if entry["passed"] is True)
        passed_count += sum(1 for entry in forbidden if entry["triggered"] is False)
        score = round(passed_count / total, 4)
        passed = execution_ok and expected_ok and criteria_ok and forbidden_ok

        evidence = list(observed.get("evidence") or []) + list(observed.get("artifact_refs") or [])
        evidence += list(checked["expected_match"]["evidence"])
        for entry in checks:
            evidence += list(entry["evidence"])
        for entry in forbidden:
            evidence += list(entry["evidence"])

        results.append(
            {
                "id": item_id,
                "status": "pass" if passed else ("error" if observed["status"] == "error" else "fail"),
                "verified": True,
                "score": score,
                "evidence": _dedupe(evidence),
                **({"notes": checked["notes"]} if checked.get("notes") else {}),
            }
        )

    final = {
        "schema_version": "2.0",
        "run_id": request["run_id"],
        "gate": request["gate"],
        "skill_id": request["skill"]["id"],
        "skill_version": request["skill"]["version"],
        "package_sha256": request["skill"]["package_sha256"],
        "definition_sha256": request["definition"]["sha256"],
        "generated_by": "skills-brain-eval-harness",
        "generated_at": _now(),
        "verification": {
            "type": verification["verification_type"],
            "verified_by": verification["verified_by"],
            "independent": True,
        },
        "results": results,
    }
    if request.get("source_commit"):
        final["source_commit"] = request["source_commit"]
    _validate(final, "eval-results.schema.json")

    if output_path is None:
        filename = "golden-results.json" if request["gate"] == "Q4" else "regression-results.json"
        output_path = skill_dir / "evals" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(final, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Skills Brain Q4/Q5 evaluation harness")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="create a content-addressed evaluation request")
    prepare.add_argument("skill_dir", type=Path)
    prepare.add_argument("--gate", choices=["Q4", "Q5"], required=True)
    prepare.add_argument("--run-id")
    prepare.add_argument("--output-dir", type=Path)

    finalize = sub.add_parser("finalize", help="consolidate runner + independent verifier evidence")
    finalize.add_argument("skill_dir", type=Path)
    finalize.add_argument("--request", type=Path, required=True)
    finalize.add_argument("--runner-results", type=Path, required=True)
    finalize.add_argument("--verification", type=Path, required=True)
    finalize.add_argument("--output", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "prepare":
            print(prepare_run(args.skill_dir, args.gate, run_id=args.run_id, output_dir=args.output_dir))
        else:
            print(
                finalize_run(
                    args.skill_dir,
                    args.request,
                    args.runner_results,
                    args.verification,
                    output_path=args.output,
                )
            )
        return 0
    except (HarnessError, FileNotFoundError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"eval-harness: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
