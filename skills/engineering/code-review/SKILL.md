---
name: code-review
description: Independently review a code change for correctness, security, tests, architecture and regression risk without modifying the repository.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.1"
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
6. Verify that tests cover the changed behavior and failure paths, not merely that the reported suite is green.
7. Identify regression and migration risks supported by visible evidence.
8. Classify findings by severity and distinguish blockers from optional suggestions.
9. Return `approve`, `changes_required`, or `block` with traceable evidence.

## Evidence and severity discipline

- **Blocker/high:** concrete security, authorization, data-integrity or production-safety defect that makes the change unsafe as proposed.
- **Mandatory change:** evidence-backed correctness/test/contract issue that must be resolved before approval.
- **Optional suggestion:** maintainability or clarity improvement that does not make the current change unsafe.

A test suite is evidence about the cases it actually covers. Missing material failure-path coverage remains a review concern even when all executed tests pass.

## Guardrails

- Do not rewrite code merely for personal style.
- Do not invent repository conventions; read the actual conventions when available.
- A green test suite does not prove a change is safe if material cases are untested.
- Do not invent unrelated vulnerabilities, migrations or operational risks outside the visible change surface.
- This Skill is read-only: do not modify the reviewed repository.
- A review verdict does not grant merge, release or deployment authority.

## Output

Return:

- verdict;
- findings ordered by severity;
- evidence/file references for every blocker or mandatory change;
- missing test/failure-path coverage;
- mandatory changes;
- optional suggestions kept separate;
- residual risks and unresolved context;
- explicit statement that merge/deploy authority remains outside the Skill.
