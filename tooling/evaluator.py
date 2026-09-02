#!/usr/bin/env python3
"""Evidence-based Skills Brain evaluator (Q0-Q5).

The evaluator never fabricates execution evidence. Q4/Q5 require result artifacts
produced by an external evaluation harness before they can pass.
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

QUALITY_GATES = {
    "Q0": {"name": "Schema", "weight": 0.20},
    "Q1": {"name": "Static quality", "weight": 0.15},
    "Q2": {"name": "Scenario definitions", "weight": 0.15},
    "Q3": {"name": "Security policy tests", "weight": 0.15},
    "Q4": {"name": "Golden task execution", "weight": 0.20},
    "Q5": {"name": "Regression evidence", "weight": 0.15},
}


def _yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _validate_document(path: Path, schema_name: str):
    if not path.exists():
        return False, [f"Missing {path.relative_to(ROOT)}"]
    try:
        data = _yaml(path) if path.suffix in {".yaml", ".yml"} else _json(path)
        schema = _json(ROOT / "schemas" / schema_name)
        jsonschema.validate(data, schema)
        return True, []
    except Exception as exc:
        return False, [str(exc)]


def check_q0(skill_dir: Path):
    from validate import validate_skill

    issues = validate_skill(skill_dir)
    return not issues, issues


def check_q1(skill_dir: Path):
    manifest = _yaml(skill_dir / "skill.yaml")
    issues = []
    risk = int(manifest["risk"]["level"])
    side_effects = manifest["side_effects"]
    security = manifest["security"]
    tools = set(manifest.get("requirements", {}).get("tool_capabilities", []))

    if security["destructive_operations"] and risk < 3:
        issues.append("destructive_operations=true requires risk >= 3")
    if side_effects == "destructive" and risk < 3:
        issues.append("side_effects=destructive requires risk >= 3")
    if security["network"]["outbound"] and "network.outbound" not in tools:
        issues.append("network.outbound security requirement must be declared as a tool capability")
    if security["filesystem"]["write"] and "filesystem.write" not in tools:
        issues.append("filesystem.write permission must be declared as a tool capability")
    if security["shell"] and "shell.execute" not in tools:
        issues.append("shell=true requires shell.execute tool capability")
    if manifest["status"] in {"approved", "active"} and manifest["evaluation"]["golden_tasks"] != "required":
        issues.append("approved/active skills must require golden tasks")

    return not issues, issues


def check_q2(skill_dir: Path):
    return _validate_document(skill_dir / "tests" / "scenarios.yaml", "scenarios.schema.json")


def check_q3(skill_dir: Path):
    manifest = _yaml(skill_dir / "skill.yaml")
    path = skill_dir / "tests" / "security.yaml"
    if manifest["risk"]["level"] < 2 and not path.exists():
        return True, ["Security test definition optional for risk < 2"]
    return _validate_document(path, "security-tests.schema.json")


def _result_gate(skill_dir: Path, definition_name: str, result_name: str, definition_schema: str, result_schema: str, optional: bool = False):
    definition_path = skill_dir / "evals" / definition_name
    result_path = skill_dir / "evals" / result_name

    if optional and not definition_path.exists():
        return True, [f"{definition_name} optional for this skill"]

    ok, issues = _validate_document(definition_path, definition_schema)
    if not ok:
        return False, issues
    ok, issues = _validate_document(result_path, result_schema)
    if not ok:
        return False, issues + ["Execution evidence is required; do not hand-author PASS results"]

    data = _json(result_path)
    failed = [item.get("id", "unknown") for item in data.get("results", []) if item.get("status") != "pass" or not item.get("verified", False)]
    if failed:
        return False, [f"Unverified or failing result(s): {', '.join(failed)}"]
    return True, []


def check_q4(skill_dir: Path):
    manifest = _yaml(skill_dir / "skill.yaml")
    mode = manifest["evaluation"]["golden_tasks"]
    if mode == "none":
        return True, ["Golden tasks explicitly disabled"]
    return _result_gate(
        skill_dir,
        "golden.yaml",
        "golden-results.json",
        "golden.schema.json",
        "eval-results.schema.json",
        optional=(mode == "optional"),
    )


def check_q5(skill_dir: Path):
    manifest = _yaml(skill_dir / "skill.yaml")
    required = manifest["status"] in {"approved", "active"} or manifest["risk"]["level"] >= 3
    return _result_gate(
        skill_dir,
        "regression.yaml",
        "regression-results.json",
        "regression.schema.json",
        "eval-results.schema.json",
        optional=not required,
    )


def evaluate_skill(skill_dir: Path):
    checks = {
        "Q0": check_q0,
        "Q1": check_q1,
        "Q2": check_q2,
        "Q3": check_q3,
        "Q4": check_q4,
        "Q5": check_q5,
    }
    results = {}
    score = 0.0
    for gate, fn in checks.items():
        try:
            passed, issues = fn(skill_dir)
        except Exception as exc:
            passed, issues = False, [str(exc)]
        results[gate] = {"passed": passed, "issues": issues}
        if passed:
            score += QUALITY_GATES[gate]["weight"]

    manifest = _yaml(skill_dir / "skill.yaml")
    minimum = float(manifest["evaluation"]["minimum_score"])
    mandatory = ["Q0", "Q1", "Q2"]
    if manifest["risk"]["level"] >= 2:
        mandatory.append("Q3")
    if manifest["evaluation"]["golden_tasks"] == "required":
        mandatory.append("Q4")
    if manifest["status"] in {"approved", "active"} or manifest["risk"]["level"] >= 3:
        mandatory.append("Q5")

    passed = score >= minimum and all(results[gate]["passed"] for gate in mandatory)
    return {
        "score": round(score, 2),
        "minimum_score": minimum,
        "mandatory_gates": mandatory,
        "quality_gates": results,
        "passed": passed,
    }


def iter_skill_dirs():
    return sorted({path.parent for path in SKILLS_ROOT.rglob("skill.yaml")})


def evaluate_all_skills():
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    all_results = {}
    for skill_dir in iter_skill_dirs():
        manifest = _yaml(skill_dir / "skill.yaml")
        skill_id = manifest.get("id", str(skill_dir.relative_to(SKILLS_ROOT)))
        result = evaluate_skill(skill_dir)
        all_results[skill_id] = result
        mark = "PASS" if result["passed"] else "FAIL"
        print(f"{skill_id}: {result['score']:.2f}/{result['minimum_score']:.2f} {mark}")
    with (reports_dir / "evaluation.json").open("w", encoding="utf-8") as handle:
        json.dump(all_results, handle, indent=2, ensure_ascii=False)
    return all_results


if __name__ == "__main__":
    evaluate_all_skills()
