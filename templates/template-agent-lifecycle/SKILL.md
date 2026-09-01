---
name: template-agent-lifecycle
description: Use this skill when the user wants to create, update, or delete an AgenticOS agent following the standard lifecycle. Triggers on "cré«« un agent", "nouvel agent", "update agent", "supprime un agent", "agent lifecycle". Do NOT use this skill for non-AgenticOS agents, or for tasks unrelated to agent lifecycle (e.g., running an agent, debugging agent code).
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: templates
---

# Template: Agent Lifecycle

## Purpose

Provides a standardized workflow for creating, updating, and deleting agents in AgenticOS. This is a template skill — adapt it to your specific agent structure.

## When to use / When NOT to use

**Use this skill when:**
- Creating a new agent with standard AgenticOS structure
- Updating an existing agent (config, code, dependencies)
- Deleting an agent with proper cleanup

**Do NOT use this skill for:**
- Non-AgenticOS agents
- Running or debugging agent code (use `agenticos-agent-audit` for that)
- Migration of agent data between versions (use `template-migration`)

## Workflow

### CREATE (new agent)

1. **Validate agent name** — kebab-case, unique within `instances/`
2. **Scaffold structure** — create `instances/<agent-name>/` with standard subdirs
3. **Generate config** — `agent.yaml` with name, version, entry point, dependencies
4. **Initialize code** — `main.py` or `index.js` with boilerplate
5. **Register agent** — add to `instances/registry.json` if applicable
6. **Validate** — run `agenticos-agent-audit` on the new agent

### UPDATE (existing agent)

1. **Locate agent** — find in `instances/<agent-name>/`
2. **Backup** — create timestamped backup before changes
3. **Apply changes** — config, code, or dependencies as requested
4. **Validate** — run `agenticos-agent-audit` post-update
5. **Document** — update `CHANGELOG.md` in agent directory

### DELETE (remove agent)

1. **Confirm** — explicit user confirmation required
2. **Backup** — archive agent directory before deletion
3. **Unregister** — remove from `instances/registry.json`
4. **Delete** — remove `instances/<agent-name>/`
5. **Verify** — confirm agent no longer appears in listings

## Rules

- Never create an agent without running `agenticos-agent-audit` afterward
- Always backup before UPDATE or DELETE
- Agent names must be kebab-case and unique
- Config must include: name, version, entry_point, dependencies

## Examples

### Happy path (CREATE)

- **Input:** "Cré«« un agent `zabbix-proxi-monitor` pour surveiller les proxies"
- **Expected:** Scaffold `instances/zabbix-proxi-monitor/`, generate config + boilerplate, register, validate
- **Actual:** Structure created, audit PASS
- **Status:** PASS
- **Validation level:** L1 static

### Edge case (UPDATE with breaking change)

- **Input:** "Mets à jour `invoice-processor` pour changer le schema de données"
- **Expected:** Backup first, apply changes, run migration if needed, validate
- **Actual:** Backup created, migration suggested, audit PASS after changes
- **Status:** PASS
- **Validation level:** L1 static

### Stress case (DELETE production agent)

- **Input:** "Supprime `legacy-ocr-agent`"
- **Expected:** Explicit confirmation requested, backup created, unregister, delete, verify
- **Actual:** Confirmation obtained, backup archived, agent removed, audit confirms deletion
- **Status:** PASS
- **Validation level:** L1 static

## References

- `agenticos-agent-audit` (validation skill)
- `template-migration` (for schema/data migrations)
- AgenticOS `instances/` structure documentation
