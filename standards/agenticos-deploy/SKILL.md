---
name: agenticos-deploy
description: Use this skill when the user wants to deploy or rollback an AgenticOS agent. Triggers on "deploy agent", "rollback agent", "deploy", "rollback". Do NOT use for non-AgenticOS agents or non-deployment tasks.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: standards
---

# Standard: AgenticOS Deploy

## Purpose

Deploys or rollbacks an AgenticOS agent with validation and safety checks.

## Workflow

### DEPLOY

1. Validate agent exists in `instances/<agent-name>/`
2. Run `agenticos-agent-audit` — must PASS (no CRITICAL)
3. Backup current deployment
4. Deploy to target environment (dev/staging/prod)
5. Health check post-deploy
6. Report status

### ROLLBACK

1. Confirm target version to rollback to
2. Backup current state
3. Restore previous version
4. Health check post-rollback
5. Report status

## Rules

- Never deploy without audit PASS
- Always backup before deploy/rollback
- Prod requires explicit confirmation

## Examples

### Happy path (deploy)
- **Input:** "Deploy `zabbix-proxi-monitor` to staging"
- **Expected:** Audit, backup, deploy, health check
- **Actual:** Deployed, health OK
- **Status:** PASS · Level: L1

### Edge case (audit fail)
- **Input:** "Deploy `broken-agent` to prod"
- **Expected:** Block deploy, show CRITICAL findings
- **Actual:** Blocked, audit CRITICAL shown
- **Status:** PASS · Level: L1

### Stress case (rollback prod)
- **Input:** "Rollback `payment-agent` on prod"
- **Expected:** Explicit confirmation, backup, rollback, verify
- **Actual:** Confirmed, rolled back, health OK
- **Status:** PASS · Level: L1

## References

- `agenticos-agent-audit`
- `template-agent-lifecycle`
