---
name: release-readiness
description: Assess release readiness from explicit evidence across quality, security, operations and rollback criteria.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.1"
  category: engineering
---

# Release Readiness

## Purpose

Determine whether a release candidate has enough evidence to proceed, with every readiness gate classified explicitly and unknown evidence preserved as unknown rather than silently passing.

## Gate model

Every gate is exactly one of:

- **PASS** — direct current evidence satisfies the criterion;
- **FAIL** — direct current evidence shows the criterion is not satisfied;
- **UNVERIFIED** — the required evidence is missing, stale, incomplete or not attributable.

`UNVERIFIED` is not a weaker form of PASS. A failed mandatory gate is not erased by an aggregate score or by unrelated successful gates.

## Workflow

1. Enumerate the readiness criteria before assessing the candidate.
2. Map available evidence to each quality, security, migration, observability, operational and rollback gate.
3. Classify every gate as PASS, FAIL or UNVERIFIED and retain the concrete evidence behind the classification.
4. Identify dependencies between gates and any risk that invalidates an apparent pass.
5. Separate release-blocking findings from accepted residual risk.
6. Require explicit rollback/recovery evidence when the change can affect production state.
7. Identify approvals or risk exceptions that must come from an external runtime/human authority.
8. Return `ready`, `not_ready` or `insufficient_evidence` while preserving the authority boundary for the actual release action.

## Decision semantics

- A known mandatory **FAIL** makes the release `not_ready`.
- A material mandatory **UNVERIFIED** gate makes the release `not_ready` or `insufficient_evidence` according to the supplied policy; it never becomes PASS automatically.
- A release may be recommended `ready` only when required gates are backed by current passing evidence and no blocking conflict remains.
- A `ready` recommendation is advisory; it is not deployment authorization.

## Guardrails

- Missing evidence never counts as PASS.
- A green unit-test suite cannot substitute for security, migration, staging or rollback evidence.
- Tested rollback does not justify ignoring a known failed readiness gate.
- Do not authorize or execute deployment; this Skill only evaluates readiness.
- High-impact exceptions must be explicit, attributable to an external approval authority and retained as residual risk.
- Do not hide failed/unverified gates inside an aggregate score.

## Output

Return:

- readiness recommendation;
- gate matrix with PASS / FAIL / UNVERIFIED;
- evidence reference for each gate;
- blockers;
- unverified/missing gates;
- residual risks;
- migration/rollback evidence when relevant;
- required external approvals/exceptions;
- explicit statement that deployment authority remains outside the Skill.
