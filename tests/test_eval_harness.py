import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("eval_harness", ROOT / "tooling" / "eval_harness.py")
harness = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(harness)


def _skill(tmp_path: Path) -> Path:
    skill = tmp_path / "example-skill"
    (skill / "evals").mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Example Skill\n\nEvidence-first example.\n", encoding="utf-8")
    (skill / "skill.yaml").write_text(
        "schema_version: \"2.1\"\n"
        "id: example-skill\n"
        "version: 1.0.0\n",
        encoding="utf-8",
    )
    (skill / "evals" / "golden.yaml").write_text(
        "schema_version: \"1.0\"\n"
        "tasks:\n"
        "  - id: evidence-first\n"
        "    mission: Analyze a finding using only supplied evidence.\n"
        "    expected:\n"
        "      verdict: evidence_based\n"
        "    forbidden:\n"
        "      - invent missing evidence\n"
        "    criteria:\n"
        "      - Separates observation from recommendation.\n",
        encoding="utf-8",
    )
    (skill / "evals" / "regression.yaml").write_text(
        "schema_version: \"1.0\"\n"
        "baseline: example-skill@0.9.0\n"
        "checks:\n"
        "  - id: quality-floor\n"
        "    metric: verified_success_rate\n"
        "    allowed_delta: -0.02\n"
        "    direction: higher-is-better\n",
        encoding="utf-8",
    )
    return skill


def _runner(run_id: str, path: Path, generated_by: str = "agenticos-eval-runner") -> Path:
    payload = {
        "schema_version": "1.0",
        "run_id": run_id,
        "generated_by": generated_by,
        "generated_at": "2026-09-02T10:00:00Z",
        "runtime": "agenticos",
        "model": "test-model",
        "results": [
            {
                "id": "evidence-first",
                "status": "completed",
                "output_summary": "Evidence and recommendation were separated.",
                "artifact_refs": ["artifact://execution/evidence-first"],
                "evidence": ["trace://run/evidence-first"],
            }
        ],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _verification(run_id: str, path: Path, verified_by: str = "independent-reviewer", independent: bool = True) -> Path:
    payload = {
        "schema_version": "1.0",
        "run_id": run_id,
        "verified_by": verified_by,
        "verification_type": "independent_model",
        "generated_at": "2026-09-02T10:05:00Z",
        "independent": independent,
        "results": [
            {
                "id": "evidence-first",
                "expected_match": {"passed": True, "evidence": ["review://expected"]},
                "criteria_checks": [
                    {
                        "criterion": "Separates observation from recommendation.",
                        "passed": True,
                        "evidence": ["review://criterion/1"],
                    }
                ],
                "forbidden_checks": [
                    {
                        "rule": "invent missing evidence",
                        "triggered": False,
                        "evidence": ["review://forbidden/1"],
                    }
                ],
            }
        ],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_prepare_and_finalize_verified_q4(tmp_path):
    skill = _skill(tmp_path)
    request_path = harness.prepare_run(skill, "Q4", run_id="example-q4-0001", output_dir=tmp_path / "run")
    request = json.loads(request_path.read_text(encoding="utf-8"))
    assert request["skill"]["id"] == "example-skill"
    assert len(request["skill"]["package_sha256"]) == 64
    assert request["items"][0]["kind"] == "golden_task"

    runner = _runner(request["run_id"], tmp_path / "runner.json")
    verification = _verification(request["run_id"], tmp_path / "verification.json")
    output = tmp_path / "golden-results.json"
    harness.finalize_run(skill, request_path, runner, verification, output_path=output)
    result = json.loads(output.read_text(encoding="utf-8"))

    assert result["schema_version"] == "2.0"
    assert result["verification"]["independent"] is True
    assert result["results"][0]["status"] == "pass"
    assert result["results"][0]["verified"] is True
    assert result["results"][0]["score"] == 1.0


def test_finalize_rejects_same_runner_and_verifier_identity(tmp_path):
    skill = _skill(tmp_path)
    request_path = harness.prepare_run(skill, "Q4", run_id="example-q4-0002", output_dir=tmp_path / "run")
    runner = _runner("example-q4-0002", tmp_path / "runner.json", generated_by="same-actor")
    verification = _verification("example-q4-0002", tmp_path / "verification.json", verified_by="same-actor")
    with pytest.raises(harness.HarnessError, match="identities must differ"):
        harness.finalize_run(skill, request_path, runner, verification, output_path=tmp_path / "out.json")


def test_finalize_rejects_skill_changed_after_prepare(tmp_path):
    skill = _skill(tmp_path)
    request_path = harness.prepare_run(skill, "Q4", run_id="example-q4-0003", output_dir=tmp_path / "run")
    (skill / "SKILL.md").write_text("# Changed after execution request\n", encoding="utf-8")
    runner = _runner("example-q4-0003", tmp_path / "runner.json")
    verification = _verification("example-q4-0003", tmp_path / "verification.json")
    with pytest.raises(harness.HarnessError, match="package changed"):
        harness.finalize_run(skill, request_path, runner, verification, output_path=tmp_path / "out.json")


def test_finalize_rejects_incomplete_criterion_coverage(tmp_path):
    skill = _skill(tmp_path)
    request_path = harness.prepare_run(skill, "Q4", run_id="example-q4-0004", output_dir=tmp_path / "run")
    runner = _runner("example-q4-0004", tmp_path / "runner.json")
    verification = json.loads(_verification("example-q4-0004", tmp_path / "verification.json").read_text(encoding="utf-8"))
    verification["results"][0]["criteria_checks"][0]["criterion"] = "Different criterion"
    verification_path = tmp_path / "bad-verification.json"
    verification_path.write_text(json.dumps(verification), encoding="utf-8")
    with pytest.raises(harness.HarnessError, match="criterion coverage mismatch"):
        harness.finalize_run(skill, request_path, runner, verification_path, output_path=tmp_path / "out.json")


def test_prepare_q5_normalizes_regression_definition(tmp_path):
    skill = _skill(tmp_path)
    request_path = harness.prepare_run(skill, "Q5", run_id="example-q5-0001", output_dir=tmp_path / "run-q5")
    request = json.loads(request_path.read_text(encoding="utf-8"))
    assert request["gate"] == "Q5"
    assert request["items"][0]["kind"] == "regression_check"
    assert request["items"][0]["input"]["baseline"] == "example-skill@0.9.0"
    assert request["items"][0]["input"]["metric"] == "verified_success_rate"
