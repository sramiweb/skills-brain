---
name: agenticos-security-scan
description: Perform evidence-based security scanning for AgenticOS deployments without mutating production state.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "1.0.0"
  category: agenticos
---

# AgenticOS Security Scan

## Purpose

Identify vulnerabilities, unsafe configuration and policy mismatches using authorized read-oriented security tooling. Findings must be traceable to evidence.

## Workflow

1. Define scope and authorized targets.
2. Collect configuration and security evidence through approved tools.
3. Separate confirmed vulnerabilities from hypotheses and informational findings.
4. Map findings to affected components and severity.
5. Identify required remediation and validation steps.
6. Escalate security veto conditions to AgenticOS policy/decision layers.
7. Produce a report without modifying the target.

## Inputs

- Authorized deployment or configuration scope.
- Security requirements/policies.
- Scan evidence.

## Outputs

- Security findings with evidence.
- Severity/confidence.
- Remediation recommendations.
- Blocking/veto recommendation when justified.

## Guardrails

- Read-only by default.
- Never scan assets outside explicit scope.
- Never claim a vulnerability is fixed without verification evidence.
- A Council consensus cannot override a confirmed security veto.
