---
name: postgres-diagnosis
description: Diagnose PostgreSQL health and performance from metrics, query evidence, locks and observed symptoms.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: databases
---

# PostgreSQL Diagnosis

## Purpose

Diagnose PostgreSQL incidents and performance degradation from observable evidence while keeping remediation separate from diagnosis.

## Workflow

1. Define the symptom, impact window and affected workload before looking for causes.
2. Inspect saturation signals, connections, transaction age, lock waits, query latency and error evidence when available.
3. Separate database symptoms from host, storage, network and application symptoms.
4. Rank hypotheses by how well they explain the complete evidence set.
5. For each hypothesis, identify confirming and disconfirming checks.
6. Detect dangerous conditions such as long-running transactions, blocking chains, replication lag or exhausted resources without automatically acting on them.
7. Return safe read-only next checks and mark remediation as a separate authorized activity.

## Guardrails

- Do not recommend killing sessions, changing parameters or running destructive SQL without explicit runtime authorization.
- Do not diagnose from one metric in isolation.
- Treat query text and database contents according to the runtime data-class policy.
- Distinguish correlation from root cause.

## Output

Incident summary, ranked hypotheses, supporting/contradicting evidence, missing signals, likely impact, confidence and safe next diagnostic checks.
