#!/usr/bin/env python3
"""Export a canonical Skills Brain skill as an AgenticOS governance contract.

This adapter never grants runtime permissions. It exports canonical requirements,
typed data contracts, governance metadata and deterministic integrity hashes for
AgenticOS to bind locally.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tooling.integrity import calculate  # noqa: E402

COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")


def load_manifest(skill_dir: Path) -> dict:
    data = yaml.safe_load((skill_dir / "skill.yaml").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("skill.yaml must contain a YAML object")
    return data


def build_export(skill_dir: Path, repository: str, commit: str) -> dict:
    skill_dir = skill_dir.resolve()
    if not repository.strip():
        raise ValueError("repository must not be empty")
    if not COMMIT_RE.fullmatch(commit):
        raise ValueError("commit must be a lowercase 40-character Git SHA")

    try:
        rel_path = skill_dir.relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise ValueError("skill_dir must be inside the Skills Brain repository") from exc
    if not rel_path.startswith("skills/"):
        raise ValueError("only canonical skills under skills/ can be exported")

    manifest = load_manifest(skill_dir)
    requirements = manifest.get("requirements") or {}
    contracts = manifest.get("contracts") or {}

    return {
        "contract_version": "1.1",
        "source": {
            "repository": repository,
            "commit": commit,
            "path": rel_path,
        },
        "skill": {
            "id": manifest["id"],
            "aliases": list(manifest.get("aliases") or []),
            "version": manifest["version"],
            "status": manifest["status"],
            "description": manifest["description"],
            "capabilities": list(manifest.get("capabilities") or []),
            "requirements": {
                "tool_capabilities": list(requirements.get("tool_capabilities") or []),
                "skills": list(requirements.get("skills") or []),
            },
            "contracts": {
                "inputs": list(contracts.get("inputs") or []),
                "outputs": list(contracts.get("outputs") or []),
            },
            "compatibility": dict(manifest.get("compatibility") or {}),
        },
        "governance": {
            "risk": dict(manifest.get("risk") or {}),
            "side_effects": manifest.get("side_effects", "none"),
            "security": dict(manifest.get("security") or {}),
            "data_classes": dict(manifest.get("data_classes") or {}),
            "evaluation": dict(manifest.get("evaluation") or {}),
        },
        "integrity": calculate(skill_dir),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Skills Brain metadata for AgenticOS")
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("--repository", required=True, help="Source repository, e.g. sramiweb/skills-brain")
    parser.add_argument("--commit", required=True, help="Resolved 40-character source commit")
    parser.add_argument("--output", type=Path, help="Optional output JSON file; stdout is used by default")
    args = parser.parse_args()

    payload = build_export(args.skill_dir, args.repository, args.commit)
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
