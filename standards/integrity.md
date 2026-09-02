# Skills Brain Package Integrity

Skills Brain packages must be reproducible and verifiable by downstream runtimes such as AgenticOS.

## Hashes

Three hashes are defined:

- `skill_sha256`: SHA-256 of the exact UTF-8 bytes of `SKILL.md`.
- `manifest_sha256`: SHA-256 of canonical JSON produced from `skill.yaml` after removing the optional top-level `integrity` field.
- `package_sha256`: SHA-256 of the deterministic package stream described below.

The `integrity` field is excluded from manifest/package hashing to avoid a self-referential hash.

## Canonical manifest representation

1. Parse `skill.yaml` as YAML.
2. Remove top-level `integrity` if present.
3. Serialize as UTF-8 JSON with:
   - keys sorted recursively;
   - separators `,` and `:` with no insignificant whitespace;
   - Unicode preserved rather than ASCII escaped.
4. Hash the resulting bytes.

## Package hash

The package hash is **fail-closed by inclusion**: every regular file below the Skill directory is included unless it matches an explicit exclusion below. This prevents new directories such as `scripts/`, `resources/`, `fixtures/` or `assets/` from silently escaping integrity coverage.

Explicitly excluded:

- `.git/**`;
- `__pycache__/**`, `.pytest_cache/**`, `.mypy_cache/**`, `.ruff_cache/**`;
- Python bytecode (`*.pyc`, `*.pyo`);
- `.DS_Store` and editor backup files ending in `~`;
- generated evaluation result evidence named `*-results.json`;
- generated verified regression baseline evidence named `regression-baseline.json`;
- the optional top-level `integrity` field inside `skill.yaml`.

Generated evaluation evidence is excluded because it describes measurements **about** an immutable package rather than source instructions that define the package. Adding Q4/Q5 results or a verified regression baseline must therefore not mutate the identity of the Skill being evaluated. The evidence has its own schemas, hashes, verifier identity and governance lifecycle.

This exclusion does **not** apply to evaluation definitions such as `golden.yaml`, `regression.yaml`, scenario/security definitions or fixtures. Those files define how the Skill is evaluated and remain part of `package_sha256`; changing them invalidates stale evaluation evidence as intended.

Files are processed in lexicographic order using relative POSIX paths. For each file, the package stream appends:

```text
<relative-path-utf8>\0<content-length-as-ascii>\0<content-bytes>
```

For `skill.yaml`, `content-bytes` are the canonical manifest bytes rather than the original YAML formatting.

## Runtime rule

AgenticOS must verify the package hash after installation and before exposing the Skill to a worker. A mismatch is fail-closed.

A runtime must pin both:

```text
source commit/tag resolution
+
package_sha256
```

The runtime must not execute upstream repository code to compute trust; it may implement this published algorithm independently.
