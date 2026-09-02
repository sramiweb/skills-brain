---
name: application-health
description: Diagnose application health by correlating infrastructure, application telemetry and business-flow checks.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: sre
---

# Application Health

## Purpose

Determine whether an application is actually healthy. A running process or HTTP 200 is not sufficient when critical business workflows are failing.

## Workflow

1. Establish the observation window and freshness requirement.
2. Check infrastructure signals such as CPU, memory, disk, network, containers/processes and database connectivity when supplied.
3. Check application signals such as API errors, latency, background jobs, queues and authentication.
4. Check business-flow signals for critical workflows supplied by the product context.
5. Correlate anomalies across layers.
6. Classify health as `healthy`, `degraded`, `critical`, or `insufficient-evidence`.
7. Recommend the least risky next diagnostic/remediation step.
8. After any authorized remediation, verify with fresh technical and business evidence.

## Guardrails

- Do not mark the system healthy solely from process/HTTP availability.
- Do not use stale evidence as current state.
- Diagnosis does not authorize restart, deployment or database mutation.
- Preserve uncertainty and conflicting signals.

## Output

Health classification, affected layers, evidence, probable/confirmed causes, missing evidence and recommended next steps.
