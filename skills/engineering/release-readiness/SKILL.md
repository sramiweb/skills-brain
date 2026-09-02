---
name: release-readiness
description: Assess release readiness from explicit evidence across quality, security, operations and rollback criteria.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: engineering
---

# Release Readiness

## Purpose

Determine whether a release candidate has enough evidence to proceed, with unknown gates treated as unknown rather than silently passing.

## Workflow

1. Enumerate the readiness criteria before assessing the candidate.
2. Map available evidence to each quality, security, migration, observability and rollback gate.
3. Classify every gate as pass, fail or unverified.
4. Identify dependencies between gates and any risk that invalidates an apparent pass.
5. Separate release-blocking findings from accepted residual risk.
6. Require explicit rollback/recovery evidence when the change can affect production state.
7. Return a recommendation while preserving the runtime/human authority that makes the actual release decision.

## Guardrails

- Missing evidence never counts as PASS.
- A green unit-test suite cannot substitute for security, migration or rollback evidence.
- Do not authorize deployment; this Skill only evaluates readiness.
- High-impact exceptions must be explicit and attributable to an approval authority.

## Output

Readiness recommendation, gate matrix, blockers, unverified gates, residual risks, rollback evidence and required approvals.
