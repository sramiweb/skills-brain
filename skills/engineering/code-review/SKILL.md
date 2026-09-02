---
name: code-review
description: Independently review a code change for correctness, security, tests, architecture and regression risk without modifying the repository.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: engineering
---

# Code Review

## Purpose

Provide an independent review of a proposed change. The reviewer must not approve its own implementation in a high-impact workflow.

## Workflow

1. Understand the intended behavior and acceptance criteria.
2. Inspect the diff and only the surrounding code required to validate it.
3. Check correctness, edge cases and data integrity.
4. Check authentication/authorization, secrets, injection and unsafe external effects where relevant.
5. Evaluate architecture/convention consistency and maintainability.
6. Verify that tests cover the changed behavior and failure paths.
7. Identify regression and migration risks.
8. Return `approve`, `changes_required`, or `block` with evidence.

## Guardrails

- Do not rewrite code merely for personal style.
- Do not invent repository conventions; read the actual conventions when available.
- A green test suite does not prove a change is safe if material cases are untested.
- The review itself does not merge, deploy or modify files.

## Output

Verdict, findings by severity, evidence/file references, mandatory changes, optional suggestions and residual risks.
