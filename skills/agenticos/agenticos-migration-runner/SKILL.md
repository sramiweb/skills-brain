---
name: agenticos-migration-runner
description: Plan and run governed database or service migrations with explicit preflight, rollback and verification requirements.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "1.0.0"
  category: agenticos
---

# AgenticOS Migration Runner

## Purpose

Guide high-risk migrations while preserving separation between planning, authorization and execution. A migration is not considered successful until post-change verification passes.

## Workflow

1. Identify migration objective, exact target version/state and affected components.
2. Validate migration artifacts before execution.
3. Verify backup/recovery prerequisites and define a tested rollback strategy.
4. Assess locks, downtime, data integrity and compatibility risks relevant to the target.
5. Produce a technical debate/review package for high-risk production migrations.
6. Obtain AgenticOS/human approval required by policy.
7. Execute only through authorized mutable tools with idempotency controls where possible.
8. Verify schema/data/application health after the migration.
9. Roll back or escalate when acceptance criteria fail.
10. Record the outcome and trigger retrospective learning.

## Inputs

- Migration artifacts or change description.
- Target environment/context.
- Backup and rollback evidence.
- Acceptance criteria.

## Outputs

- Migration plan and risk assessment.
- Execution/verification evidence when authorized.
- Rollback or escalation result.

## Guardrails

- Never generate a claim that rollback is possible unless the rollback path is actually defined.
- Production database mutation requires explicit runtime authorization.
- Never retry a non-idempotent migration blindly.
- Never mark a migration successful solely because the migration command exited successfully.
