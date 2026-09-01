---
name: agenticos-agent-create
description: Use this skill when the user wants to create a new AgenticOS agent with standard structure. Triggers on "cré«« un agent", "nouvel agent", "new agent", "scaffold agent". Do NOT use for updating/deleting agents or non-AgenticOS agents.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: standards
---

# Standard: AgenticOS Agent Create

## Purpose

Creates a new AgenticOS agent with standard structure, config, and boilerplate.

## Workflow

1. Validate name (kebab-case, unique)
2. Scaffold `instances/<agent-name>/` with agent.yaml, main.py, requirements.txt, README.md, tests/
3. Generate config with name, version, entry_point
4. Initialize main.py boilerplate
5. Register in instances/registry.json
6. Validate with agenticos-agent-audit

## Rules

- Kebab-case only
- No overwrite without confirmation
- Always audit after creation

## Examples

### Happy path
- **Input:** "Cré«« un agent `zabbix-proxi-monitor`"
- **Expected:** Scaffold, config, validate
- **Actual:** Created, audit PASS
- **Status:** PASS · Level: L1

### Edge case (conflict)
- **Input:** "Cré«« un agent `invoice-processor`" (exists)
- **Expected:** Detect conflict, prompt user
- **Actual:** Conflict detected
- **Status:** PASS · Level: L1

### Stress case (invalid name)
- **Input:** "Cré«« un agent `My_Agent_123`"
- **Expected:** Reject, suggest kebab-case
- **Actual:** Rejected, `my-agent-123` suggested
- **Status:** PASS · Level: L1

## References

- `template-agent-lifecycle`
- `agenticos-agent-audit`
