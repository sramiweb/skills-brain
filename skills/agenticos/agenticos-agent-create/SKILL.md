---
name: agenticos-agent-create
description: Design a new AgenticOS agent definition from purpose, capabilities and governance constraints.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "1.0.0"
  category: agenticos
---

# AgenticOS Agent Create

## Purpose

Design a governed AgenticOS agent configuration. This Skill may produce configuration artifacts or proposals, but it does not grant itself permissions and does not activate an agent outside AgenticOS policy.

## Workflow

1. Define purpose, domain, inputs, outputs and success metrics.
2. Identify required capabilities before selecting concrete tools.
3. Select primary/supporting Skills from the governed registry.
4. Propose data class, runtime, quotas, triggers and memory mode.
5. Derive the minimum required connector/tool capabilities.
6. Define forbidden actions, approval policy and debate/learning policy.
7. Run independent audit/review before activation.

## Inputs

- Agent purpose and domain.
- Required capabilities.
- Tenant/runtime constraints supplied by AgenticOS.
- Risk and data classification constraints.

## Outputs

- Agent definition proposal.
- Required Skill/capability list.
- Governance checklist.
- Validation findings.

## Guardrails

- Never grant permissions not explicitly authorized by AgenticOS.
- Never embed credentials or tenant secrets in a canonical Skill.
- Prefer a Worker/Skill over a new permanent agent when responsibility does not justify a separate owner.
- Creator must not be the final reviewer for high-impact agents.
