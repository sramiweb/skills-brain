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


composer = load_module("skills_brain_composer", ROOT / "tooling" / "composer.py")


def write_manifest(root: Path, name: str, capability: str, **overrides):
    skill_dir = root / name
    skill_dir.mkdir(parents=True)
    manifest = {
        "id": name,
        "version": "1.0.0",
        "status": "candidate",
        "capabilities": [capability],
        "risk": {"level": 1},
        "side_effects": "none",
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
        "capabilities": ["product.discover", "product.feature.specify"],
        "available_tool_capabilities": ["filesystem.read"],
        "allowed_status": ["candidate", "approved", "active"],
        "max_risk": 2,
        "data_class": "S2",
        "runtime": {"name": "agenticos", "version": "3.1", "require_explicit_compatibility": True},
        "evaluation_report": str(report_path),
        "max_skills": 5,
        "include_rejected": True,
    }


def write_report(path: Path, scores: dict[str, float]):
    path.write_text(json.dumps({skill_id: {"score": score} for skill_id, score in scores.items()}), encoding="utf-8")


def discovery_output(data_class="S2"):
    return {
        "outputs": [{
            "id": "discovery-result",
            "schema_id": "product.discovery-result.v1",
            "data_class": data_class,
        }]
    }


def specification_input(allowed=None):
    return {
        "inputs": [{
            "id": "discovery-result",
            "schema_id": "product.discovery-result.v1",
            "source": "skill",
            "required": True,
            "from_capabilities": ["product.discover"],
            "allowed_data_classes": allowed or ["S1", "S2"],
        }]
    }


def test_composes_smallest_eligible_set_and_never_grants_authorization(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "discovery", "product.discover")
    write_manifest(skills, "specification", "product.feature.specify")
    write_manifest(skills, "extra-discovery", "product.discover")
    report = tmp_path / "evaluation.json"
    write_report(report, {"discovery": 0.9, "specification": 0.8, "extra-discovery": 0.2})

    result = composer.compose(base_request(report), skills_root=skills)

    assert result["status"] == "composed"
    assert result["authorization"] == "not_granted"
    assert [item["id"] for item in result["selected_skills"]] == ["discovery", "specification"]
    assert result["handoffs"] == []
    assert result["missing_capabilities"] == []
    assert result["blocking_reasons"] == []


def test_prefers_one_full_match_over_unnecessary_bundle(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(
        skills,
        "full",
        "product.discover",
        capabilities=["product.discover", "product.feature.specify"],
    )
    write_manifest(skills, "discovery", "product.discover")
    write_manifest(skills, "specification", "product.feature.specify")
    report = tmp_path / "evaluation.json"
    write_report(report, {"full": 0.4, "discovery": 1.0, "specification": 1.0})

    result = composer.compose(base_request(report), skills_root=skills)

    assert result["status"] == "composed"
    assert [item["id"] for item in result["selected_skills"]] == ["full"]


def test_declared_dependency_is_closed_and_ordered_before_parent(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "discovery", "product.discover")
    write_manifest(
        skills,
        "specification",
        "product.feature.specify",
        requirements={"tool_capabilities": [], "skills": ["analysis"]},
    )
    write_manifest(skills, "analysis", "engineering.codebase.analyze")
    report = tmp_path / "evaluation.json"
    write_report(report, {"discovery": 0.8, "specification": 0.8, "analysis": 0.8})

    result = composer.compose(base_request(report), skills_root=skills)

    assert result["status"] == "composed"
    assert set(result["execution_order"]) == {"discovery", "analysis", "specification"}
    assert result["execution_order"].index("analysis") < result["execution_order"].index("specification")
    analysis = next(item for item in result["selected_skills"] if item["id"] == "analysis")
    assert analysis["dependency"] is True


def test_ineligible_dependency_blocks_composition(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "discovery", "product.discover")
    write_manifest(
        skills,
        "specification",
        "product.feature.specify",
        requirements={"tool_capabilities": [], "skills": ["analysis"]},
    )
    write_manifest(
        skills,
        "analysis",
        "engineering.codebase.analyze",
        requirements={"tool_capabilities": ["logs.read"]},
    )
    report = tmp_path / "evaluation.json"
    write_report(report, {"discovery": 0.8, "specification": 0.8, "analysis": 1.0})

    result = composer.compose(base_request(report), skills_root=skills)

    assert result["status"] == "unresolved"
    assert result["selected_skills"] == []
    assert any(reason.startswith("dependency_ineligible:specification->analysis:missing_tools:") for reason in result["blocking_reasons"])


def test_explicit_conflict_blocks_otherwise_complete_composition(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(
        skills,
        "discovery",
        "product.discover",
        relationships={"conflicts": ["specification"]},
    )
    write_manifest(skills, "specification", "product.feature.specify")
    report = tmp_path / "evaluation.json"
    write_report(report, {"discovery": 0.9, "specification": 0.9})

    result = composer.compose(base_request(report), skills_root=skills)

    assert result["status"] == "unresolved"
    assert "conflict:discovery:specification" in result["blocking_reasons"]
    assert result["authorization"] == "not_granted"


def test_dependency_closure_respects_total_max_skills(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "discovery", "product.discover")
    write_manifest(
        skills,
        "specification",
        "product.feature.specify",
        requirements={"tool_capabilities": [], "skills": ["analysis"]},
    )
    write_manifest(skills, "analysis", "engineering.codebase.analyze")
    report = tmp_path / "evaluation.json"
    write_report(report, {"discovery": 0.8, "specification": 0.8, "analysis": 0.8})
    request = base_request(report)
    request["max_skills"] = 2

    result = composer.compose(request, skills_root=skills)

    assert result["status"] == "unresolved"
    assert "max_skills_exceeded:3>2" in result["blocking_reasons"]


def test_missing_eligible_capability_is_reported_without_adjacent_substitution(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "discovery", "product.discover")
    report = tmp_path / "evaluation.json"
    write_report(report, {"discovery": 1.0})

    result = composer.compose(base_request(report), skills_root=skills)

    assert result["status"] == "unresolved"
    assert result["missing_capabilities"] == ["product.feature.specify"]
    assert result["selected_skills"] == []


def test_typed_handoff_creates_data_edge_and_orders_producer_first(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "discovery", "product.discover", contracts=discovery_output("S2"))
    write_manifest(skills, "specification", "product.feature.specify", contracts=specification_input(["S1", "S2"]))
    report = tmp_path / "evaluation.json"
    write_report(report, {"discovery": 0.8, "specification": 0.8})

    result = composer.compose(base_request(report), skills_root=skills)

    assert result["status"] == "composed"
    assert result["execution_order"].index("discovery") < result["execution_order"].index("specification")
    assert result["handoffs"] == [{
        "producer_skill": "discovery",
        "output": "discovery-result",
        "consumer_skill": "specification",
        "input": "discovery-result",
        "schema_id": "product.discovery-result.v1",
        "data_class": "S2",
    }]


def test_required_typed_handoff_blocks_when_schema_provider_is_missing(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "discovery", "product.discover")
    write_manifest(skills, "specification", "product.feature.specify", contracts=specification_input(["S2"]))
    report = tmp_path / "evaluation.json"
    write_report(report, {"discovery": 0.8, "specification": 0.8})

    result = composer.compose(base_request(report), skills_root=skills)

    assert result["status"] == "unresolved"
    assert result["selected_skills"] == []
    assert "handoff_unresolved:specification:discovery-result:product.discovery-result.v1" in result["blocking_reasons"]


def test_typed_handoff_blocks_data_class_widening(tmp_path):
    skills = tmp_path / "skills"
    write_manifest(skills, "discovery", "product.discover", contracts=discovery_output("S3"))
    write_manifest(skills, "specification", "product.feature.specify", contracts=specification_input(["S0", "S1", "S2"]))
    report = tmp_path / "evaluation.json"
    write_report(report, {"discovery": 0.8, "specification": 0.8})

    result = composer.compose(base_request(report), skills_root=skills)

    assert result["status"] == "unresolved"
    assert "handoff_data_class_denied:specification:discovery-result:S3" in result["blocking_reasons"]
