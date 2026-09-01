---
name: agenticos-agent-audit
description: Use this skill when the user wants to audit an AgenticOS agent for compliance, security, and best practices. Triggers on "audit agent", "check agent", "validate agent". Do NOT use for non-AgenticOS agents.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: standards
---

# Standard: AgenticOS Agent Audit

## Purpose

Audits an AgenticOS agent for structure, config, security, and best practices.

## Workflow

1. Locate agent in `instances/<agent-name>/`
2. Check structure (agent.yaml, main.py, README.md, tests/)
3. Validate config (name, version, entry_point)
4. Security scan (secrets, credentials)
5. Code quality (lint, imports)
6. Report CRITICAL/WARNING/INFO

## Examples

### Happy path
- **Input:** "Audit `zabbix-proxi-monitor`"
- **Expected:** All checks PASS
- **Actual:** PASS
- **Status:** PASS · Level: L1

### Edge case (missing file)
- **Input:** "Audit `incomplete-agent`"
- **Expected:** WARNING for missing README
- **Actual:** WARNING
- **Status:** PASS · Level: L1

### Stress case (security)
- **Input:** "Audit `leaky-agent`"
- **Expected:** CRITICAL for hardcoded secret
- **Actual:** CRITICAL
- **Status:** PASS · Level: L1

## References

- `template-agent-lifecycle`
- `agenticos-agent-create`
