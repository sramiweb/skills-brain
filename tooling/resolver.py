#!/usr/bin/env python3
"""Skills Brain Resolver v2 - Match capabilities et rank skills"""
import json
from pathlib import Path

def load_catalog():
    catalog_dir = Path(__file__).parent.parent / "catalog"
    index_path = catalog_dir / "index.json"
    deps_path = catalog_dir / "dependencies.json"
    if not index_path.exists():
        raise FileNotFoundError("Run catalog.py first")
    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)
    deps = json.load(open(deps_path, "r", encoding="utf-8")) if deps_path.exists() else {}
    return index, deps

def find_skills_for_capabilities(required_caps, index, deps):
    matches = {}
    for skill_id, skill_data in index.items():
        skill_caps = set(skill_data.get("capabilities", []))
        matched_caps = skill_caps.intersection(set(required_caps))
        if matched_caps:
            matches[skill_id] = {
                "matched": list(matched_caps),
                "coverage": len(matched_caps) / len(required_caps) if required_caps else 0,
                "skill_data": skill_data,
                "dependencies": deps.get(skill_id, {}),
            }
    return matches

def rank_skills(matches):
    ranked = []
    for skill_id, match_data in matches.items():
        score = match_data["skill_data"].get("quality_score", 0.0)
        risk = match_data["skill_data"].get("risk_level", 0)
        coverage = match_data["coverage"]
        composite = (coverage * 0.5) + (score * 0.4) - (risk * 0.1)
        ranked.append({
            "skill_id": skill_id,
            "composite_score": round(composite, 3),
            "quality_score": score,
            "risk_level": risk,
            "coverage": coverage,
            "matched_capabilities": match_data["matched"],
        })
    ranked.sort(key=lambda x: x["composite_score"], reverse=True)
    return ranked

def resolve_capabilities(required_caps, top_n=5):
    index, deps = load_catalog()
    eval_path = Path(__file__).parent.parent / "reports" / "evaluation.json"
    eval_results = json.load(open(eval_path, "r", encoding="utf-8")) if eval_path.exists() else {}
    for skill_id, eval_data in eval_results.items():
        if skill_id in index:
            index[skill_id]["quality_score"] = eval_data.get("score", 0.0)
    matches = find_skills_for_capabilities(required_caps, index, deps)
    if not matches:
        print(f"❌ No skills found for: {required_caps}")
        return []
    ranked = rank_skills(matches)
    print(f"✅ Found {len(ranked)} skills for {len(required_caps)} capabilities:")
    for i, skill in enumerate(ranked[:top_n], 1):
        print(f"  {i}. {skill['skill_id']} (score: {skill['composite_score']:.3f}, coverage: {skill['coverage']:.1%})")
    return ranked

if __name__ == "__main__":
    import sys
    caps = sys.argv[1:] if len(sys.argv) > 1 else ["deployment.orchestration", "security.scanning"]
    resolve_capabilities(caps)
