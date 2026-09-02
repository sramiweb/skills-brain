#!/usr/bin/env python3
"""Governed runtime qualification workflow for Skills Brain Q4/Q5.

This CLI coordinates content-addressed preparation, runtime adapter planning,
observation collection and finalization. It never executes AgenticOS or an LLM
itself and never acts as the independent verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


harness = _load_module("skills_brain_eval_harness", ROOT / "tooling" / "eval_harness.py")
agenticos = _load_module("skills_brain_agenticos_eval", ROOT / "adapters" / "agenticos" / "evaluation.py")
integrity = _load_module("skills_brain_integrity_qualification", ROOT / "tooling" / "integrity.py")


class QualificationError(RuntimeError):
    pass


def _json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise QualificationError(f"{path}: expected JSON object")
    return data


def _yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise QualificationError(f"{path}: expected YAML object")
    return data


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate(data: dict, schema_name: str) -> None:
    schema = _json(ROOT / "schemas" / schema_name)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    if errors:
        raise QualificationError(
            f"{schema_name}: " + "; ".join(error.message for error in errors[:8])
        )


def _baseline_for(skill_dir: Path, baseline_path: Path | None) -> tuple[Path, dict]:
    path = baseline_path or (skill_dir / "evals" / "regression-baseline.json")
    path = path.resolve()
    if not path.exists():
        raise QualificationError(
            "Q5 requires verified regression baseline evidence. "
            f"Missing {path}; do not invent historical metric values."
        )
    baseline = _json(path)
    _validate(baseline, "regression-baseline.schema.json")
    if baseline.get("verified") is not True or (baseline.get("verification") or {}).get("independent") is not True:
        raise QualificationError("Q5 baseline must be independently verified")
    return path, baseline


def _bind_q5_baseline(skill_dir: Path, request_path: Path, baseline_path: Path | None) -> dict:
    request = _json(request_path)
    regression = _yaml(skill_dir / "evals" / "regression.yaml")
    path, baseline = _baseline_for(skill_dir, baseline_path)
    if baseline["baseline_id"] != regression["baseline"]:
        raise QualificationError(
            f"baseline id mismatch: regression expects {regression['baseline']}, got {baseline['baseline_id']}"
        )

    metrics = baseline["metrics"]
    for item in request["items"]:
        metric = (item.get("input") or {}).get("metric")
        if metric not in metrics:
            raise QualificationError(f"baseline missing metric required by Q5: {metric}")
        item["input"]["baseline_value"] = metrics[metric]["value"]
        item["input"]["baseline_evidence_refs"] = metrics[metric]["evidence_refs"]

    request["baseline"] = {
        "id": baseline["baseline_id"],
        "path": str(path),
        "sha256": _sha256(path),
    }
    _validate(request, "eval-run.schema.json")
    request_path.write_text(
        json.dumps(request, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return request


def prepare(
    skill_dir: Path,
    gate: str,
    *,
    tenant: str,
    agent: str,
    data_class: str,
    model: str | None,
    output_dir: Path | None,
    baseline_path: Path | None,
) -> dict:
    skill_dir = skill_dir.resolve()
    request_path = harness.prepare_run(skill_dir, gate, output_dir=output_dir)
    request = _json(request_path)
    if gate.upper() == "Q5":
        request = _bind_q5_baseline(skill_dir, request_path, baseline_path)

    plan = agenticos.build_plan(
        request,
        tenant=tenant,
        agent=agent,
        data_class=data_class,
        model=model,
    )
    plan_path = request_path.parent / "agenticos-plan.json"
    plan_path.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "run_id": request["run_id"],
        "gate": request["gate"],
        "skill": request["skill"],
        "source_commit": request.get("source_commit"),
        "request": str(request_path),
        "agenticos_plan": str(plan_path),
        "baseline": request.get("baseline"),
        "authorization": "not_granted",
    }


def collect(request_path: Path, observation_path: Path, output_path: Path | None) -> dict:
    request = _json(request_path)
    observation = _json(observation_path)
    runner = agenticos.collect_runner_results(request, observation)
    target = output_path or (request_path.parent / "runner-results.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(runner, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {"run_id": request["run_id"], "runner_results": str(target)}


def _verify_bound_baseline(request: dict) -> None:
    bound = request.get("baseline")
    if not bound:
        if request.get("gate") == "Q5":
            raise QualificationError("Q5 request is not bound to verified baseline evidence")
        return
    path = Path(bound["path"])
    if not path.exists():
        raise QualificationError(f"bound Q5 baseline no longer exists: {path}")
    if _sha256(path) != bound["sha256"]:
        raise QualificationError("Q5 baseline changed since preparation; prepare a new run")
    baseline = _json(path)
    _validate(baseline, "regression-baseline.schema.json")
    if baseline["baseline_id"] != bound["id"]:
        raise QualificationError("Q5 baseline identity changed since preparation")


def finalize(
    skill_dir: Path,
    request_path: Path,
    runner_results_path: Path,
    verification_path: Path,
    output_path: Path | None,
) -> dict:
    request = _json(request_path)
    _verify_bound_baseline(request)
    target = harness.finalize_run(
        skill_dir,
        request_path,
        runner_results_path,
        verification_path,
        output_path=output_path,
    )
    return {"run_id": request["run_id"], "gate": request["gate"], "result": str(target)}


def status(skill_dir: Path) -> dict:
    skill_dir = skill_dir.resolve()
    manifest = _yaml(skill_dir / "skill.yaml")
    hashes = integrity.calculate(skill_dir)
    evals = skill_dir / "evals"
    q4_definition = evals / "golden.yaml"
    q4_result = evals / "golden-results.json"
    q5_definition = evals / "regression.yaml"
    q5_result = evals / "regression-results.json"
    baseline = evals / "regression-baseline.json"
    return {
        "skill": {
            "id": manifest["id"],
            "version": str(manifest["version"]),
            "status": manifest["status"],
            **hashes,
        },
        "Q4": {
            "definition": q4_definition.exists(),
            "verified_result": q4_result.exists(),
            "ready_to_prepare": q4_definition.exists(),
        },
        "Q5": {
            "definition": q5_definition.exists(),
            "verified_result": q5_result.exists(),
            "verified_baseline": baseline.exists(),
            "ready_to_prepare": q5_definition.exists() and baseline.exists(),
        },
        "authorization": "not_granted",
    }


def _print(data: dict) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Skills Brain governed runtime qualification")
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status")
    p_status.add_argument("skill_dir", type=Path)

    p_prepare = sub.add_parser("prepare")
    p_prepare.add_argument("skill_dir", type=Path)
    p_prepare.add_argument("--gate", choices=["Q4", "Q5"], required=True)
    p_prepare.add_argument("--tenant", required=True)
    p_prepare.add_argument("--agent", required=True)
    p_prepare.add_argument("--data-class", choices=["S0", "S1", "S2", "S3"], required=True)
    p_prepare.add_argument("--model")
    p_prepare.add_argument("--output-dir", type=Path)
    p_prepare.add_argument("--baseline", type=Path)

    p_collect = sub.add_parser("collect")
    p_collect.add_argument("--request", type=Path, required=True)
    p_collect.add_argument("--observation", type=Path, required=True)
    p_collect.add_argument("--output", type=Path)

    p_finalize = sub.add_parser("finalize")
    p_finalize.add_argument("skill_dir", type=Path)
    p_finalize.add_argument("--request", type=Path, required=True)
    p_finalize.add_argument("--runner-results", type=Path, required=True)
    p_finalize.add_argument("--verification", type=Path, required=True)
    p_finalize.add_argument("--output", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "status":
            payload = status(args.skill_dir)
        elif args.command == "prepare":
            payload = prepare(
                args.skill_dir,
                args.gate,
                tenant=args.tenant,
                agent=args.agent,
                data_class=args.data_class,
                model=args.model,
                output_dir=args.output_dir,
                baseline_path=args.baseline,
            )
        elif args.command == "collect":
            payload = collect(args.request, args.observation, args.output)
        else:
            payload = finalize(
                args.skill_dir,
                args.request,
                args.runner_results,
                args.verification,
                args.output,
            )
        _print(payload)
        return 0
    except Exception as exc:
        print(f"qualification: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
