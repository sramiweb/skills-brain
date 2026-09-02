import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLING = ROOT / "tooling"
sys.path.insert(0, str(TOOLING))

harness_spec = importlib.util.spec_from_file_location("eval_harness_for_evaluator", TOOLING / "eval_harness.py")
harness = importlib.util.module_from_spec(harness_spec)
assert harness_spec and harness_spec.loader
harness_spec.loader.exec_module(harness)

evaluator_spec = importlib.util.spec_from_file_location("evaluator_under_test", TOOLING / "evaluator.py")
evaluator = importlib.util.module_from_spec(evaluator_spec)
assert evaluator_spec and evaluator_spec.loader
evaluator_spec.loader.exec_module(evaluator)


def _skill(tmp_path: Path) -> Path:
    skill = tmp_path / "verified-skill"
    (skill / "evals").mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Verified Skill\n", encoding="utf-8")
    (skill / "skill.yaml").write_text(
        "schema_version: \"2.1\"\n"
        "id: verified-skill\n"
        "version: 1.0.0\n"
        "evaluation:\n"
        "  golden_tasks: required\n"
        "  minimum_score: 0.90\n",
        encoding="utf-8",
    )
    (skill / "evals" / "golden.yaml").write_text(
        "schema_version: \"1.0\"\n"
        "tasks:\n"
        "  - id: one\n"
        "    mission: Produce an evidence-based answer.\n"
        "    expected: {verdict: ok}\n"
        "    criteria:\n"
        "      - Uses supplied evidence.\n",
        encoding="utf-8",
    )
    return skill


def _write_external_evidence(tmp_path: Path, run_id: str):
    runner = tmp_path / "runner.json"
    runner.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "run_id": run_id,
                "generated_by": "runtime-runner",
                "generated_at": "2026-09-02T10:00:00Z",
                "results": [{"id": "one", "status": "completed", "evidence": ["trace://one"]}],
            }
        ),
        encoding="utf-8",
    )
    verification = tmp_path / "verification.json"
    verification.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "run_id": run_id,
                "verified_by": "independent-reviewer",
                "verification_type": "human",
                "generated_at": "2026-09-02T10:05:00Z",
                "independent": True,
                "results": [
                    {
                        "id": "one",
                        "expected_match": {"passed": True, "evidence": ["review://expected"]},
                        "criteria_checks": [
                            {"criterion": "Uses supplied evidence.", "passed": True, "evidence": ["review://criterion"]}
                        ],
                        "forbidden_checks": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return runner, verification


def test_evaluator_accepts_current_harness_evidence_and_rejects_stale_package(tmp_path):
    skill = _skill(tmp_path)
    request = harness.prepare_run(skill, "Q4", run_id="verified-q4-0001", output_dir=tmp_path / "run")
    runner, verification = _write_external_evidence(tmp_path, "verified-q4-0001")
    harness.finalize_run(skill, request, runner, verification)

    passed, issues = evaluator.check_q4(skill)
    assert passed is True, issues

    (skill / "SKILL.md").write_text("# Changed after verified evaluation\n", encoding="utf-8")
    passed, issues = evaluator.check_q4(skill)
    assert passed is False
    assert any("package_sha256" in issue for issue in issues)


def test_evaluator_rejects_definition_changed_after_verified_run(tmp_path):
    skill = _skill(tmp_path)
    request = harness.prepare_run(skill, "Q4", run_id="verified-q4-0002", output_dir=tmp_path / "run")
    runner, verification = _write_external_evidence(tmp_path, "verified-q4-0002")
    harness.finalize_run(skill, request, runner, verification)

    golden = skill / "evals" / "golden.yaml"
    golden.write_text(golden.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    passed, issues = evaluator.check_q4(skill)
    assert passed is False
    assert any("definition_sha256" in issue or "package_sha256" in issue for issue in issues)
