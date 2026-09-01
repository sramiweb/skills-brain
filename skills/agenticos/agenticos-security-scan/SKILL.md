---
name: "Agenticos Security Scan"
version: "1.0.0"
status: "active"
---

# Agenticos Security Scan

Security scanning skill for AgenticOS deployments.

## Purpose

This skill performs comprehensive security scans on AgenticOS deployments, identifying vulnerabilities, misconfigurations, and compliance issues.

## Workflow

1. **Discovery**: Scan deployment for exposed endpoints and services
2. **Analysis**: Run security checks against identified resources
3. **Reporting**: Generate detailed security report with findings
4. **Remediation**: Provide actionable remediation steps

## Inputs

- `deployment_target`: Target deployment URL or identifier
- `scan_depth`: Depth of scan (shallow, medium, deep)
- `compliance_framework`: Optional compliance framework (SOC2, ISO27001, etc.)

## Outputs

- `security_report`: JSON report with findings
- `risk_score`: Overall risk score (0-100)
- `remediation_plan`: Prioritized list of fixes

## Examples

```yaml
# Run security scan
skill: agenticos/security-scan
inputs:
  deployment_target: "prod-us-east-1"
  scan_depth: "deep"
  compliance_framework: "SOC2"
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
