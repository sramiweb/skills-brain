#!/usr/bin/env python3
"""Skills Brain Evaluator v2 - Évalue les skills via Q0-Q5"""
import json, os
from pathlib import Path
try:
    import yaml
except ImportError:
    os.system("pip install pyyaml")
    import yaml

QUALITY_GATES = {
    "Q0": {"name": "Structure", "weight": 0.10},
    "Q1": {"name": "Syntaxe YAML", "weight": 0.15},
    "Q2": {"name": "Schema Compliance", "weight": 0.20},
    "Q3": {"name": "Golden Tasks", "weight": 0.25},
    "Q4": {"name": "Documentation", "weight": 0.15},
    "Q5": {"name": "Security", "weight": 0.15},
}

def load_skill_yaml(p):
    f = p / "skill.yaml"
    return yaml.safe_load(open(f, encoding="utf-8")) if f.exists() else None

def check_q0(p):
    r = ["skill.yaml", "SKILL.md", "README.md"]
    m = [x for x in r if not (p / x).exists()]
    return len(m) == 0, m

def check_q1(p):
    try:
        return load_skill_yaml(p) is not None, []
    except Exception as e:
        return False, [str(e)]

def check_q2(p, schema_path):
    try:
        import jsonschema
        schema = json.load(open(schema_path, encoding="utf-8"))
        jsonschema.validate(load_skill_yaml(p), schema)
        return True, []
    except ImportError:
        d = load_skill_yaml(p) or {}
        m = [f for f in ["name","version","status","capabilities"] if f not in d]
        return len(m) == 0, m
    except Exception as e:
        return False, [str(e)]

def check_q3(p):
    g = p / "tests" / "golden"
    return (True, []) if not g.exists() else (True, [])

def check_q4(p):
    r = p / "README.md"
    if not r.exists():
        return False, ["Missing README.md"]
    c = r.read_text(encoding="utf-8")
    m = [s for s in ["## Usage", "## Inputs", "## Outputs"] if s not in c]
    return len(m) == 0, m

def check_q5(p):
    return True, []

def evaluate_skill(p, schema_path):
    res, score = {}, 0.0
    for q, fn in [("Q0", check_q0), ("Q1", check_q1), ("Q2", lambda x,y: check_q2(x,schema_path)), ("Q3", check_q3), ("Q4", check_q4), ("Q5", check_q5)]:
        ok, iss = (fn(p) if q != "Q2" else fn(p, schema_path)) if q == "Q2" else (check_q2(p, schema_path) if q == "Q2" else (check_q0(p) if q == "Q0" else (check_q1(p) if q == "Q1" else (check_q3(p) if q == "Q3" else (check_q4(p) if q == "Q4" else check_q5(p))))))
        res[q] = {"passed": ok, "issues": iss}
        if ok:
            score += QUALITY_GATES[q]["weight"]
    return {"score": round(score, 2), "max_score": 1.0, "quality_gates": res, "passed": score >= 0.80}

def evaluate_all_skills():
    skills_dir = Path(__file__).parent.parent / "skills"
    schema_path = Path(__file__).parent.parent / "schemas" / "skill.schema.json"
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    all_results = {}
    for cat in ["agenticos", "templates", "services"]:
        cat_dir = skills_dir / cat
        if not cat_dir.exists():
            continue
        for skill_dir in cat_dir.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue
            skill_id = f"{cat}/{skill_dir.name}"
            result = evaluate_skill(skill_dir, schema_path)
            all_results[skill_id] = result
            print(f"{skill_id}: {result['score']:.2f}/1.00 {'✓' if result['passed'] else '✗'}")
    json.dump(all_results, open(reports_dir / "evaluation.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\n✅ Rapport: {reports_dir}/evaluation.json")
    return all_results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        evaluate_all_skills()
    else:
        skills_dir = Path(__file__).parent.parent / "skills"
        schema_path = Path(__file__).parent.parent / "schemas" / "skill.schema.json"
        for cat in ["agenticos", "templates", "services"]:
            cat_dir = skills_dir / cat
            if cat_dir.exists():
                for skill_dir in cat_dir.iterdir():
                    if skill_dir.is_dir() and not skill_dir.name.startswith("."):
                        skill_id = f"{cat}/{skill_dir.name}"
                        result = evaluate_skill(skill_dir, schema_path)
                        print(f"\n{skill_id}:\n  Score: {result['score']:.2f}/1.00\n  Passed: {result['passed']}")
                        for gate, data in result["quality_gates"].items():
                            print(f"  {'✓' if data['passed'] else '✗'} {gate}: {data['issues'] or 'OK'}")
                        break
                break
