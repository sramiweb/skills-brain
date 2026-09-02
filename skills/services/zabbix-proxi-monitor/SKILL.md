---
name: zabbix-proxy-monitor
description: Diagnose Zabbix proxy health and synchronization problems from observable monitoring and log evidence.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "1.0.0"
  category: services
  external: zabbix
---

# Zabbix Proxy Monitor

## Purpose

Diagnose Zabbix proxy availability, configuration synchronization and data-flow health without assuming that a single HTTP/process status proves the proxy is healthy.

## Workflow

1. Establish the exact proxy and observation window.
2. Collect fresh proxy/server health evidence and relevant logs through authorized tools.
3. Check availability, backlog/queue symptoms, configuration synchronization and database/runtime errors.
4. Correlate symptoms before proposing a root cause.
5. Distinguish confirmed root cause, likely cause and missing evidence.
6. Recommend the least risky next diagnostic or remediation step.
7. Verify any authorized remediation with fresh evidence.

## Inputs

- Proxy identifier/context.
- Fresh health/monitoring state.
- Relevant proxy/server logs.
- Optional configuration synchronization evidence.

## Outputs

- Structured diagnosis.
- Evidence references.
- Confidence and missing evidence.
- Recommended next actions.

## Guardrails

- Do not restart, delete or modify proxy state from this Skill alone.
- Do not infer a root cause from one log line when correlated evidence is available.
- Stale monitoring data must not be treated as current health.
- If required evidence is unavailable, return `insufficient_evidence` rather than inventing a diagnosis.

## Examples

A recurring configuration-sync failure accompanied by database foreign-key errors should be reported as a correlated configuration/database integrity problem, not merely as "proxy down".
