---
name: "Agenticos Agent Audit"
version: "1.0.0"
status: "active"
---

# Agenticos Agent Audit

Audit agent behavior and decisions for compliance and safety.

## Purpose

This skill performs comprehensive audits of agent behavior, decisions, and outputs to ensure compliance with safety guidelines and operational policies.

## Workflow

1. **Data Collection**: Gather agent logs, decisions, and outputs
2. **Analysis**: Apply audit rules and compliance checks
3. **Reporting**: Generate audit report with findings
4. **Recommendations**: Provide actionable improvements

## Inputs

- `agent_id`: Target agent identifier
- `audit_period`: Time period to audit (e.g., "24h", "7d")
- `compliance_rules`: List of compliance rules to check

## Outputs

- `audit_report`: Detailed audit findings
- `compliance_score`: Overall compliance score (0-100)
- `recommendations`: List of recommended actions

## Examples

```yaml
skill: agenticos/agent-audit
inputs:
  agent_id: "agent-prod-001"
  audit_period: "24h"
  compliance_rules:
    - "no-pii-leak"
    - "rate-limit"
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
