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

Only package source files are included. Generated evaluation results and transient files are excluded.

Included by default:

- `SKILL.md`;
- canonicalized `skill.yaml`;
- `README.md` when present;
- `CHANGELOG.md` when present;
- `tests/**`;
- `evals/**`, except generated `*-results.json` files;
- `references/**`.

Excluded:

- `.git/**`;
- caches and bytecode;
- generated `*-results.json` evaluation evidence;
- OS/editor temporary files;
- the `integrity` field itself.

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
