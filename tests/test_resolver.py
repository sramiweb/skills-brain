import importlib.util
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


resolver = load_module("skills_brain_resolver", ROOT / "tooling" / "resolver.py")


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
    return skill_dir


def base_request(report_path: Path):
    return {
        "schema_version": "1.0",
        "capabilities": ["engineering.code.review"],
        "available_tool_capabilities": ["filesystem.read"],
        "allowed_status": ["candidate", "approved", "active"],
        "max_risk": 2,
        "data_class": "S2",
        "runtime": {"name": "agenticos", "version": "3.1", "require_explicit_compatibility": True},
        "include_rejected": True,
        "evaluation_report": str(report_path),
    }


def test_missing_tool_rejects_higher_quality_candidate(tmp_path):
    skills_root = tmp_path / "skills"
    write_manifest(skills_root, "eligible-skill")
    write_manifest(
        skills_root,
        "blocked-skill",
        requirements={"tool_capabilities": ["logs.read"]},
    )
    report = tmp_path / "evaluation.json"
    report.write_text(json.dumps({
        "eligible-skill": {"score": 0.60},
        "blocked-skill": {"score": 1.00},
    }), encoding="utf-8")

    result = resolver.resolve(base_request(report), skills_root=skills_root)

    assert result["authorization"] == "not_granted"
    assert [item["id"] for item in result["candidates"]] == ["eligible-skill"]
    blocked = next(item for item in result["rejected"] if item["id"] == "blocked-skill")
    assert any(reason.startswith("missing_tools:") for reason in blocked["rejection_reasons"])


def test_data_class_unspecified_is_denied_by_default(tmp_path):
    skills_root = tmp_path / "skills"
    write_manifest(skills_root, "no-data-class", data_classes={})
    report = tmp_path / "evaluation.json"
    report.write_text("{}", encoding="utf-8")

    result = resolver.resolve(base_request(report), skills_root=skills_root)

    assert result["candidates"] == []
    assert "data_class_unspecified" in result["rejected"][0]["rejection_reasons"]


def test_runtime_incompatibility_is_rejected(tmp_path):
    skills_root = tmp_path / "skills"
    write_manifest(skills_root, "old-runtime", compatibility={"agenticos": ">=2,<3"})
    report = tmp_path / "evaluation.json"
    report.write_text("{}", encoding="utf-8")

    result = resolver.resolve(base_request(report), skills_root=skills_root)

    assert result["candidates"] == []
    assert any(reason.startswith("runtime_incompatible:") for reason in result["rejected"][0]["rejection_reasons"])


def test_partial_matches_are_ranked_below_full_matches(tmp_path):
    skills_root = tmp_path / "skills"
    write_manifest(
        skills_root,
        "full",
        capabilities=["engineering.code.review", "engineering.codebase.analyze"],
    )
    write_manifest(skills_root, "partial", capabilities=["engineering.code.review"])
    report = tmp_path / "evaluation.json"
    report.write_text(json.dumps({"full": {"score": 0.50}, "partial": {"score": 1.00}}), encoding="utf-8")
    request = base_request(report)
    request["capabilities"] = ["engineering.code.review", "engineering.codebase.analyze"]

    result = resolver.resolve(request, skills_root=skills_root)

    assert result["full_match_available"] is True
    assert result["candidates"][0]["id"] == "full"
    assert result["candidates"][0]["full_match"] is True


def test_unknown_capability_fails_closed(tmp_path):
    report = tmp_path / "evaluation.json"
    report.write_text("{}", encoding="utf-8")
    request = base_request(report)
    request["capabilities"] = ["unknown.capability"]

    try:
        resolver.resolve(request, skills_root=tmp_path / "skills")
    except ValueError as exc:
        assert "Unknown requested capabilities" in str(exc)
    else:
        raise AssertionError("unknown capabilities must fail closed")


def test_compatibility_parser_supports_bounded_range():
    assert resolver.compatibility_satisfied(">=3.1,<4", "3.1")
    assert resolver.compatibility_satisfied(">=3.1,<4", "3.9.2")
    assert not resolver.compatibility_satisfied(">=3.1,<4", "4.0")
    assert not resolver.compatibility_satisfied("^3.1", "3.2")
