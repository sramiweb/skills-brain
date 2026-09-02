import importlib.util
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


qualification = load_module("skills_brain_qualification_test", ROOT / "tooling" / "qualification.py")
agenticos = load_module("skills_brain_agenticos_eval_test", ROOT / "adapters" / "agenticos" / "evaluation.py")

SKILL = ROOT / "skills" / "engineering" / "codebase-analysis"


def test_q4_prepare_builds_content_addressed_agenticos_plan(tmp_path):
    result = qualification.prepare(
        SKILL,
        "Q4",
        tenant="klerbot",
        agent="klerbot-coder",
        data_class="S2",
        model="glm-5.3:cloud",
        output_dir=tmp_path / "run",
        baseline_path=None,
    )
    request = json.loads(Path(result["request"]).read_text(encoding="utf-8"))
    plan = json.loads(Path(result["agenticos_plan"]).read_text(encoding="utf-8"))

    assert request["skill"]["id"] == "codebase-analysis"
    assert request["skill"]["version"] == "0.1.1"
    assert len(request["skill"]["package_sha256"]) == 64
    assert plan["authorization"] == "not_granted"
    assert plan["runtime"]["tenant"] == "klerbot"
    assert plan["runtime"]["agent"] == "klerbot-coder"
    assert len(plan["jobs"]) == 3
    assert all(job["expected_upstream"]["package_sha256"] == request["skill"]["package_sha256"] for job in plan["jobs"])
    assert all(job["package_context"]["read_only"] is True for job in plan["jobs"])


def test_q5_prepare_fails_without_verified_baseline(tmp_path):
    try:
        qualification.prepare(
            SKILL,
            "Q5",
            tenant="klerbot",
            agent="klerbot-coder",
            data_class="S2",
            model=None,
            output_dir=tmp_path / "run",
            baseline_path=tmp_path / "missing-baseline.json",
        )
    except qualification.QualificationError as exc:
        assert "requires verified regression baseline evidence" in str(exc)
    else:
        raise AssertionError("Q5 must fail closed when baseline evidence is missing")


def test_q5_prepare_binds_verified_baseline_metrics(tmp_path):
    baseline = {
        "schema_version": "1.0",
        "baseline_id": "codebase-analysis@0.1.0",
        "subject": {"skill_id": "codebase-analysis", "version": "0.1.0"},
        "generated_at": "2026-09-02T10:00:00Z",
        "generated_by": "test-baseline-builder",
        "verified": True,
        "verification": {"type": "human", "verified_by": "independent-reviewer", "independent": True},
        "metrics": {
            "verified_success_rate": {"value": 0.8, "evidence_refs": ["test://baseline/success"]},
            "unsupported_claim_rate": {"value": 0.1, "evidence_refs": ["test://baseline/claims"]},
            "policy_violation_rate": {"value": 0.0, "evidence_refs": ["test://baseline/policy"]},
        },
    }
    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text(json.dumps(baseline), encoding="utf-8")

    result = qualification.prepare(
        SKILL,
        "Q5",
        tenant="klerbot",
        agent="klerbot-coder",
        data_class="S2",
        model=None,
        output_dir=tmp_path / "run",
        baseline_path=baseline_path,
    )
    request = json.loads(Path(result["request"]).read_text(encoding="utf-8"))
    assert request["baseline"]["id"] == "codebase-analysis@0.1.0"
    by_id = {item["id"]: item for item in request["items"]}
    assert by_id["preserve-verified-success"]["input"]["baseline_value"] == 0.8
    assert by_id["prevent-unsupported-claims"]["input"]["baseline_value"] == 0.1
    assert by_id["preserve-read-only-policy"]["input"]["baseline_value"] == 0.0


def test_agenticos_collect_preserves_observation_without_judging(tmp_path):
    prepared = qualification.prepare(
        SKILL,
        "Q4",
        tenant="klerbot",
        agent="klerbot-coder",
        data_class="S2",
        model=None,
        output_dir=tmp_path / "run",
        baseline_path=None,
    )
    request = json.loads(Path(prepared["request"]).read_text(encoding="utf-8"))
    upstream = {
        "id": request["skill"]["id"],
        "version": request["skill"]["version"],
        "package_sha256": request["skill"]["package_sha256"],
    }
    if request.get("source_commit"):
        upstream["source_commit"] = request["source_commit"]

    observation = {
        "contract_version": "1.0",
        "run_id": request["run_id"],
        "generated_by": "agenticos-eval-runner",
        "generated_at": "2026-09-02T10:30:00Z",
        "runtime": {"platform": "agenticos", "version": "3.1"},
        "executions": [
            {
                "id": item["id"],
                "exec_id": f"exec-{index}",
                "status": "succeeded",
                "output": f"raw answer for {item['id']}",
                "model_used": "glm-5.3:cloud",
                "data_class": "S2",
                "effective_allowed_tools": ["aos-skills.skill_view"],
                "evidence_refs": [f"agenticos://trace/{index}"],
                "artifact_refs": [],
                "upstream_skill": dict(upstream),
            }
            for index, item in enumerate(request["items"], start=1)
        ],
    }
    runner = agenticos.collect_runner_results(request, observation)
    schema = json.loads((ROOT / "schemas" / "eval-runner-results.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(runner, schema)

    assert runner["generated_by"] == "agenticos-eval-runner"
    assert all(item["status"] == "completed" for item in runner["results"])
    assert all("score" not in item and "verified" not in item for item in runner["results"])
    assert runner["model"] == "glm-5.3:cloud"


def test_agenticos_collect_rejects_wrong_upstream_hash(tmp_path):
    prepared = qualification.prepare(
        SKILL,
        "Q4",
        tenant="klerbot",
        agent="klerbot-coder",
        data_class="S2",
        model=None,
        output_dir=tmp_path / "run",
        baseline_path=None,
    )
    request = json.loads(Path(prepared["request"]).read_text(encoding="utf-8"))
    observation = {
        "contract_version": "1.0",
        "run_id": request["run_id"],
        "generated_by": "agenticos-eval-runner",
        "generated_at": "2026-09-02T10:30:00Z",
        "runtime": {"platform": "agenticos"},
        "executions": [
            {
                "id": item["id"],
                "exec_id": f"exec-{index}",
                "status": "succeeded",
                "upstream_skill": {
                    "id": request["skill"]["id"],
                    "version": request["skill"]["version"],
                    "package_sha256": "0" * 64,
                    **({"source_commit": request["source_commit"]} if request.get("source_commit") else {}),
                },
            }
            for index, item in enumerate(request["items"], start=1)
        ],
    }
    try:
        agenticos.collect_runner_results(request, observation)
    except agenticos.AdapterError as exc:
        assert "package hash mismatch" in str(exc)
    else:
        raise AssertionError("mismatched runtime package must fail closed")
