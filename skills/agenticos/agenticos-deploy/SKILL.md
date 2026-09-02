---
name: agenticos-deploy
description: Prepare and execute a governed AgenticOS deployment with explicit verification, approval and rollback requirements.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "1.0.0"
  category: agenticos
---

# AgenticOS Deploy

## Purpose

Guide a governed deployment without assuming a specific infrastructure platform. Concrete deployment tools, environments and credentials are selected and authorized by AgenticOS bindings and MCP policy.

## Workflow

1. Identify the exact artifact/version and deployment target.
2. Verify preconditions, tests, security checks and dependency state.
3. Require an explicit rollback plan before any mutable action.
4. Build an execution plan with idempotency keys for external actions where supported.
5. Evaluate risk and request human approval when policy requires it.
6. Execute only through authorized AgenticOS/MCP tools.
7. Run technical and business smoke checks.
8. Compare expected and observed outcomes.
9. Roll back or escalate when verification fails.
10. Produce release/deployment evidence for audit and retrospective.

## Inputs

- Release artifact/version.
- Target environment supplied by AgenticOS.
- Verification criteria.
- Rollback plan.
- Effective runtime policy.

## Outputs

- Deployment plan/result.
- Verification evidence.
- Rollback/escalation status.

## Guardrails

- No floating `main`/`latest` artifact in production workflows.
- No production deployment without the required approval gate.
- No infrastructure assumption such as Kubernetes, Docker or VM unless provided by runtime context.
- A failed health check does not become success because deployment command returned zero.
