#!/usr/bin/env python3
"""Deterministic Skills Brain package hashing.

Implements standards/integrity.md. The tool is read-only and never writes hashes
into the source package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("Missing dependency PyYAML. Install requirements-dev.txt") from exc

GENERATED_RESULT_SUFFIX = "-results.json"
SOURCE_ROOTS = ("tests", "evals", "references")
OPTIONAL_ROOT_FILES = ("README.md", "CHANGELOG.md")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_manifest_bytes(skill_dir: Path) -> bytes:
    manifest_path = skill_dir / "skill.yaml"
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("skill.yaml must contain a YAML object")
    data = dict(data)
    data.pop("integrity", None)
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def included_files(skill_dir: Path) -> list[Path]:
    files: list[Path] = []
    required = skill_dir / "SKILL.md"
    manifest = skill_dir / "skill.yaml"
    for path in (required, manifest):
        if not path.is_file():
            raise FileNotFoundError(path)
        files.append(path)

    for filename in OPTIONAL_ROOT_FILES:
        path = skill_dir / filename
        if path.is_file():
            files.append(path)

    for root_name in SOURCE_ROOTS:
        root = skill_dir / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(skill_dir).as_posix()
            if path.name.endswith(GENERATED_RESULT_SUFFIX):
                continue
            if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                continue
            if rel.endswith("~") or path.name in {".DS_Store"}:
                continue
            files.append(path)

    return sorted(set(files), key=lambda p: p.relative_to(skill_dir).as_posix())


def package_content_bytes(skill_dir: Path, path: Path) -> bytes:
    if path.name == "skill.yaml" and path.parent == skill_dir:
        return canonical_manifest_bytes(skill_dir)
    return path.read_bytes()


def package_sha256(skill_dir: Path) -> str:
    digest = hashlib.sha256()
    for path in included_files(skill_dir):
        rel = path.relative_to(skill_dir).as_posix().encode("utf-8")
        content = package_content_bytes(skill_dir, path)
        digest.update(rel)
        digest.update(b"\0")
        digest.update(str(len(content)).encode("ascii"))
        digest.update(b"\0")
        digest.update(content)
    return digest.hexdigest()


def calculate(skill_dir: Path) -> dict[str, str]:
    skill_dir = skill_dir.resolve()
    return {
        "skill_sha256": sha256((skill_dir / "SKILL.md").read_bytes()),
        "manifest_sha256": sha256(canonical_manifest_bytes(skill_dir)),
        "package_sha256": package_sha256(skill_dir),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate deterministic Skills Brain hashes")
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    print(json.dumps(calculate(args.skill_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
