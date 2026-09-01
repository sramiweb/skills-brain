---
name: template-deployment
description: Use this skill when the user wants to deploy/rollback any service. Triggers on "deploy", "rollback", "deployment template". Do NOT use for agent-specific tasks.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: templates
---

# Template: Deployment

## Purpose

Generic deployment/rollback workflow for any service.

## Workflow

1. Validate target exists
2. Pre-deploy checks (tests, lint, audit)
3. Backup current version
4. Deploy to target env
5. Post-deploy health check
6. Report status

## Examples

### Happy path
- **Input:** "Deploy `api-service` to staging"
- **Expected:** Checks, backup, deploy, health OK
- **Actual:** Deployed
- **Status:** PASS · Level: L1

## References

- `agenticos-deploy`
