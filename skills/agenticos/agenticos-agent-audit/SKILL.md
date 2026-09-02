---
name: agenticos-agent-audit
description: Audit AgenticOS agent executions, decisions and evidence without mutating runtime state.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "1.0.0"
  category: agenticos
---

# AgenticOS Agent Audit

## Purpose

Audit an AgenticOS agent or execution using observable evidence, declared policy and decision records. The Skill is read-oriented and produces findings; it does not change agent permissions or runtime configuration.

## Workflow

1. Define the audit scope, period and rules.
2. Collect available execution, decision, policy and tool evidence.
3. Separate verified facts from assumptions and missing evidence.
4. Check policy compliance, unexpected tool usage, repeated failures, human overrides and unsupported decisions.
5. Classify findings by severity and confidence.
6. Produce remediation recommendations and evidence references.

## Inputs

- Agent or execution identifier.
- Audit period or mission scope.
- Applicable policy/compliance rules.
- Execution and decision evidence.

## Outputs

- Structured audit findings.
- Evidence references.
- Severity/confidence per finding.
- Remediation recommendations.

## Guardrails

- Never infer compliance from absence of logs.
- Never mutate the audited agent.
- Never treat LLM confidence as evidence quality.
- Missing evidence must be reported explicitly.

## Examples

A request to audit an agent that used an undeclared tool should identify the tool call, compare it with effective policy and report a policy violation only when the evidence confirms the mismatch.
