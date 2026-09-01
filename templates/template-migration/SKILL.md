---
name: template-migration
description: Use this skill when the user wants to run migrations on any service. Triggers on "run migration", "migrate", "migration template". Do NOT use for agent-specific tasks.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: templates
---

# Template: Migration

## Purpose

Generic migration workflow for any service with rollback support.

## Workflow

1. Validate migration files exist
2. Backup current state
3. Run migration (up)
4. Verify success
5. Document in CHANGELOG

## Examples

### Happy path
- **Input:** "Run migration on `api-service`"
- **Expected:** Backup, migrate, verify
- **Actual:** Migration OK
- **Status:** PASS · Level: L1

## References

- `agenticos-migration-runner`
