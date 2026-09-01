---
name: template-security-audit
description: Use this skill when the user wants to audit security of any service. Triggers on "security audit", "audit security", "security template". Do NOT use for agent-specific tasks.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: templates
---

# Template: Security Audit

## Purpose

Generic security audit workflow for any service.

## Workflow

1. Scan for secrets/credentials
2. Check unsafe patterns
3. Validate permissions
4. Check dependencies
5. Report findings

## Examples

### Happy path
- **Input:** "Security audit `api-service`"
- **Expected:** Scan, report
- **Actual:** All clear
- **Status:** PASS · Level: L1

## References

- `agenticos-security-scan`
