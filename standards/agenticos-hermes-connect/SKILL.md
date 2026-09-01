---
name: agenticos-hermes-connect
description: Use this skill when the user wants to connect an AgenticOS agent to Hermes monitoring. Triggers on "connect hermes", "hermes integration", "monitoring setup". Do NOT use for non-AgenticOS agents.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: standards
---

# Standard: AgenticOS Hermes Connect

## Purpose

Connects an AgenticOS agent to Hermes monitoring (metrics, alerts, logs).

## Workflow

1. Validate agent exists
2. Generate Hermes config (metrics endpoint, alert rules)
3. Register agent in Hermes dashboard
4. Test connectivity
5. Verify metrics flowing

## Examples

### Happy path
- **Input:** "Connect `zabbix-proxi-monitor` to Hermes"
- **Expected:** Config generated, registered, metrics OK
- **Actual:** Connected, metrics flowing
- **Status:** PASS · Level: L1

## References

- `agenticos-agent-audit`
