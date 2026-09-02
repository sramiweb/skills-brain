# Changelog — codebase-analysis

## 0.1.1 — 2026-09-02

- add reproducible `fixtures/mini-service` evaluation codebase;
- add Q2 scenarios for execution-path tracing, minimum change surface and insufficient evidence;
- add explicit read-only security/negative tests;
- add Q4 Golden Tasks covering stale documentation, dependency tracing, change surface and unsupported persistence claims;
- add Q5 regression definition against `codebase-analysis@0.1.0`;
- strengthen methodology with observed / inferred / unresolved claim classification;
- explicitly forbid silent external context expansion and convenience permission widening.

No verified `golden-results.json` or `regression-results.json` is committed by this version. Those artifacts must be produced by a real external evaluation run and independent verification through `tooling/eval_harness.py`.

## 0.1.0

Initial read-only codebase-analysis candidate.
