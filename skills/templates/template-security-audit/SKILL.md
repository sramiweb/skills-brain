---
name: "Template Security Audit"
version: "1.0.0"
status: "active"
---

# Template Security Audit

Template for security audit workflows.

## Purpose

This template provides a standardized framework for conducting security audits across systems, applications, and infrastructure.

## Workflow

1. **Scope Definition**: Define audit scope and objectives
2. **Discovery**: Identify assets and vulnerabilities
3. **Analysis**: Assess risk and compliance
4. **Reporting**: Generate audit report with findings
5. **Remediation**: Provide remediation recommendations

## Inputs

- `target_systems`: List of systems to audit
- `audit_framework`: Security framework (SOC2, ISO27001, NIST)
- `depth`: Audit depth (light, standard, comprehensive)

## Outputs

- `audit_report`: Comprehensive security audit report
- `risk_matrix`: Risk assessment matrix
- `remediation_plan`: Prioritized remediation steps

## Examples

```yaml
skill: templates/security-audit
inputs:
  target_systems:
    - "prod-web-cluster"
    - "prod-db-cluster"
  audit_framework: "SOC2"
  depth: "comprehensive"
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
