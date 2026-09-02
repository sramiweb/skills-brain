import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


reputation = load_module("skills_brain_reputation", ROOT / "tooling" / "reputation.py")
resolver = load_module("skills_brain_resolver_reputation", ROOT / "tooling" / "resolver.py")


def outcome(skill_id, *, version="1.0.0", success=True, verification=0.95, tenant_hash=None, occurred_at="2026-08-30T10:00:00Z", tool_failures=0, human_override=False, verified=True):
    payload = {
        "schema_version": "1.0",
        "subject": {"type": "skill", "id": skill_id, "version": version},
        "scope": {"runtime": "agenticos"},
        "occurred_at": occurred_at,
        "expected": {"status": "success"},
        "observed": {"status": "success" if success else "failure"},
        "success": success,
        "verified": verified,
        "verification_score": verification,
        "duration_ms": 100,
        "cost": 0.01,
        "tool_failures": tool_failures,
        "human_override": human_override,
        "evidence_refs": [f"evidence:{skill_id}:{occurred_at}"],
    }
    if tenant_hash:
        payload["scope"]["tenant_hash"] = tenant_hash
    return payload


def write_outcomes(root: Path, records):
    root.mkdir(parents=True)
    for index, record in enumerate(records):
        (root / f"outcome-{index}.json").write_text(json.dumps(record), encoding="utf-8")


def write_manifest(root: Path, name: str, **overrides):
    skill_dir = root / name
    skill_dir.mkdir(parents=True)
    manifest = {
        "id": name,
        "version": "1.0.0",
        "status": "candidate",
        "capabilities": ["engineering.code.review"],
        "risk": {"level": 1},
        "requirements": {"tool_capabilities": []},
        "data_classes": {"allowed": ["S2"]},
        "compatibility": {"agenticos": ">=3.1,<4"},
    }
    manifest.update(overrides)
    (skill_dir / "skill.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")


def base_request(evaluation_path: Path, reputation_path: Path | None = None):
    request = {
        "schema_version": "1.0",
        "capabilities": ["engineering.code.review"],
        "available_tool_capabilities": ["filesystem.read"],
        "allowed_status": ["candidate", "approved", "active"],
        "max_risk": 2,
        "data_class": "S2",
        "runtime": {"name": "agenticos", "version": "3.1", "require_explicit_compatibility": True},
        "include_rejected": True,
        "evaluation_report": str(evaluation_path),
    }
    if reputation_path:
        request["reputation_report"] = str(reputation_path)
    return request


def test_global_reputation_uses_only_verified_generic_outcomes(tmp_path):
    outcomes = tmp_path / "outcomes"
    records = [outcome("reviewer", success=True) for _ in range(5)]
    records += [
        outcome("reviewer", success=False, tenant_hash="tenant-a"),
        outcome("reviewer", success=False, verified=False),
        outcome("reviewer", success=False, verification=0.2),
    ]
    write_outcomes(outcomes, records)

    report = reputation.aggregate(
        outcomes,
        scope_type="global",
        minimum_samples=5,
        as_of=datetime(2026, 9, 2, tzinfo=timezone.utc),
    )
    item = report["subjects"]["reviewer"]

    assert report["scope"] == {"type": "global"}
    assert item["samples"] == 5
    assert item["eligible_for_ranking"] is True
    assert item["verified_success_rate"] == 1.0
    assert item["reputation_score"] is not None
    assert item["reputation_score"] < 1.0  # Wilson lower bound prevents naive certainty.


def test_below_minimum_samples_is_visible_but_not_rankable(tmp_path):
    outcomes = tmp_path / "outcomes"
    write_outcomes(outcomes, [outcome("reviewer") for _ in range(3)])

    report = reputation.aggregate(
        outcomes,
        minimum_samples=5,
        as_of=datetime(2026, 9, 2, tzinfo=timezone.utc),
    )
    item = report["subjects"]["reviewer"]

    assert item["samples"] == 3
    assert item["eligible_for_ranking"] is False
    assert item["reputation_score"] is None


def test_tenant_reputation_is_scoped_to_exact_pseudonymous_tenant(tmp_path):
    outcomes = tmp_path / "outcomes"
    write_outcomes(outcomes, [
        outcome("reviewer", tenant_hash="tenant-a") for _ in range(5)
    ] + [
        outcome("reviewer", success=False, tenant_hash="tenant-b") for _ in range(5)
    ])

    report = reputation.aggregate(
        outcomes,
        scope_type="tenant",
        tenant_hash="tenant-a",
        minimum_samples=5,
        as_of=datetime(2026, 9, 2, tzinfo=timezone.utc),
    )

    assert report["scope"] == {"type": "tenant", "tenant_hash": "tenant-a"}
    assert report["subjects"]["reviewer"]["verified_success_rate"] == 1.0


def test_reputation_refines_ranking_only_after_eligibility(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "steady")
    write_manifest(skills, "strong-runtime")
    evaluation = tmp_path / "evaluation.json"
    evaluation.write_text(json.dumps({
        "steady": {"score": 0.8},
        "strong-runtime": {"score": 0.8},
    }), encoding="utf-8")

    outcomes = tmp_path / "outcomes"
    write_outcomes(outcomes, [
        outcome("steady", success=False, human_override=True) for _ in range(5)
    ] + [
        outcome("strong-runtime", success=True) for _ in range(8)
    ])
    report = reputation.aggregate(outcomes, minimum_samples=5, as_of=datetime(2026, 9, 2, tzinfo=timezone.utc))
    reputation_path = tmp_path / "reputation.json"
    reputation_path.write_text(json.dumps(report), encoding="utf-8")

    result = resolver.resolve(base_request(evaluation, reputation_path), skills_root=skills)

    assert result["reputation_evidence_used"] is True
    assert result["candidates"][0]["id"] == "strong-runtime"
    assert result["candidates"][0]["reputation_samples"] == 8


def test_high_reputation_cannot_bypass_missing_tool(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "eligible")
    write_manifest(skills, "blocked", requirements={"tool_capabilities": ["logs.read"]})
    evaluation = tmp_path / "evaluation.json"
    evaluation.write_text(json.dumps({"eligible": {"score": 0.5}, "blocked": {"score": 1.0}}), encoding="utf-8")

    outcomes = tmp_path / "outcomes"
    write_outcomes(outcomes, [outcome("blocked", success=True) for _ in range(20)])
    report = reputation.aggregate(outcomes, minimum_samples=5, as_of=datetime(2026, 9, 2, tzinfo=timezone.utc))
    reputation_path = tmp_path / "reputation.json"
    reputation_path.write_text(json.dumps(report), encoding="utf-8")

    result = resolver.resolve(base_request(evaluation, reputation_path), skills_root=skills)

    assert [candidate["id"] for candidate in result["candidates"]] == ["eligible"]
    blocked = next(item for item in result["rejected"] if item["id"] == "blocked")
    assert blocked["reputation_score"] is not None
    assert any(reason.startswith("missing_tools:") for reason in blocked["rejection_reasons"])


def test_reputation_for_old_skill_version_is_not_used(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "reviewer", version="2.0.0")
    evaluation = tmp_path / "evaluation.json"
    evaluation.write_text(json.dumps({"reviewer": {"score": 0.8}}), encoding="utf-8")

    outcomes = tmp_path / "outcomes"
    write_outcomes(outcomes, [outcome("reviewer", version="1.0.0") for _ in range(10)])
    report = reputation.aggregate(outcomes, minimum_samples=5, as_of=datetime(2026, 9, 2, tzinfo=timezone.utc))
    reputation_path = tmp_path / "reputation.json"
    reputation_path.write_text(json.dumps(report), encoding="utf-8")

    result = resolver.resolve(base_request(evaluation, reputation_path), skills_root=skills)

    assert result["candidates"][0]["reputation_score"] is None
    assert result["candidates"][0]["reputation_samples"] == 10


def test_canonical_resolver_rejects_tenant_scoped_reputation(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "reviewer")
    evaluation = tmp_path / "evaluation.json"
    evaluation.write_text(json.dumps({"reviewer": {"score": 0.8}}), encoding="utf-8")
    outcomes = tmp_path / "outcomes"
    write_outcomes(outcomes, [outcome("reviewer", tenant_hash="tenant-a") for _ in range(5)])
    report = reputation.aggregate(
        outcomes,
        scope_type="tenant",
        tenant_hash="tenant-a",
        minimum_samples=5,
        as_of=datetime(2026, 9, 2, tzinfo=timezone.utc),
    )
    reputation_path = tmp_path / "reputation.json"
    reputation_path.write_text(json.dumps(report), encoding="utf-8")

    try:
        resolver.resolve(base_request(evaluation, reputation_path), skills_root=skills)
    except ValueError as exc:
        assert "runtime-local" in str(exc)
    else:
        raise AssertionError("tenant reputation must not influence canonical resolver")
