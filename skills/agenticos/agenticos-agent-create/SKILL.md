---
name: "Agenticos Agent Create"
version: "1.0.0"
status: "active"
---

# Agenticos Agent Create

Create and configure new AgenticOS agents with proper permissions.

## Purpose

This skill creates new AgenticOS agents with appropriate configurations, permissions, and registrations with the orchestrator.

## Workflow

1. **Validation**: Validate agent configuration and permissions
2. **Creation**: Create agent instance with specified configuration
3. **Registration**: Register agent with orchestrator
4. **Verification**: Confirm agent is operational

## Inputs

- `agent_name`: Name for the new agent
- `agent_type`: Type of agent (worker, supervisor, specialist)
- `permissions`: List of permissions to grant
- `config`: Agent configuration object

## Outputs

- `agent_id`: Created agent identifier
- `status`: Creation status (success/failure)
- `config_applied`: Applied configuration

## Examples

```yaml
skill: agenticos/agent-create
inputs:
  agent_name: "worker-agent-042"
  agent_type: "worker"
  permissions:
    - "read:files"
    - "write:files"
  config:
    max_concurrent: 5
```

## Quality Gates

- **Q0**: Structure ✓
- **Q1**: YAML Syntax ✓
- **Q2**: Schema Compliance ✓
- **Q3**: Scenarios (TODO)
- **Q4**: Golden Tasks (TODO)
- **Q5**: Security Scan ✓

## Changelog

- **1.0.0** (2026-09-01): Initial v2 release
