---
name: agenticos-security-scan
description: Use this skill when the user wants to scan an AgenticOS agent for security issues. Triggers on "security scan", "scan agent", "check secrets", "security audit". Do NOT use for non-AgenticOS agents or non-security tasks.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: standards
---

# Standard: AgenticOS Security Scan

## Purpose

Scans an AgenticOS agent for security vulnerabilities, secrets, and unsafe patterns.

## Workflow

1. Locate agent in `instances/<agent-name>/`
2. Scan for hardcoded secrets (API keys, passwords, tokens)
3. Check for unsafe patterns (eval, exec, shell injection)
4. Validate permissions and access controls
5. Check dependencies for known vulnerabilities
6. Report CRITICAL/WARNING/INFO

## Rules

- CRITICAL = immediate fix required
- WARNING = fix before production
- Never commit code with CRITICAL findings

## Examples

### Happy path
- **Input:** "Security scan `zabbix-proxi-monitor`"
- **Expected:** No secrets, no unsafe patterns
- **Actual:** All clear
- **Status:** PASS · Level: L1

### Edge case (test secrets)
- **Input:** "Security scan `test-agent`"
- **Expected:** Detect test API keys, flag WARNING
- **Actual:** WARNING for test credentials
- **Status:** PASS · Level: L1

### Stress case (real secrets)
- **Input:** "Security scan `leaky-agent`"
- **Expected:** Detect production API key, flag CRITICAL
- **Actual:** CRITICAL for exposed secret
- **Status:** PASS · Level: L1

## References

- `agenticos-agent-audit`
- `agenticos-deploy`
