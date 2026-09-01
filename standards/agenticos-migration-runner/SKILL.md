---
name: agenticos-migration-runner
description: Use this skill when the user wants to run a migration on an AgenticOS agent. Triggers on "run migration", "migrate agent", "upgrade schema". Do NOT use for non-AgenticOS agents.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: standards
---

# Standard: AgenticOS Migration Runner

## Purpose

Runs database/schema migrations on an AgenticOS agent with rollback support.

## Workflow

1. Validate agent + migration files exist
2. Backup current state
3. Run migration (up)
4. Verify migration success
5. Document in CHANGELOG

## Examples

### Happy path
- **Input:** "Run migration on `invoice-processor`"
- **Expected:** Backup, migrate, verify
- **Actual:** Migration OK
- **Status:** PASS · Level: L1

## References

- `agenticos-agent-audit`
- `agenticos-deploy`
