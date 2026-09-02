---
name: skill-deliberator
description: Run governed multi-agent deliberation over Skill promotion, selection, composition, or high-impact changes.
license: MIT
compatibility: skills-brain, agenticos
metadata:
  author: sramiweb
  version: "1.0.0"
  category: core
---

# Skill Deliberator

## Purpose

Apply a canonical deliberation protocol to decisions that benefit from independent perspectives, adversarial review, or preserved dissent.

## Workflow

1. Build an evidence pack containing proposal, alternatives, constraints, risk, and source references.
2. Select the protocol: strategic, technical, or operational.
3. Run round 1 independently: participants do not see each other's answers.
4. Normalize claims, evidence references, assumptions, confidence, and falsifiers.
5. Run cross-examination only on material disagreements.
6. Allow participants to revise their positions with a reason for change.
7. Apply security/risk veto rules.
8. Send anonymized positions to an independent judge when configured.
9. Preserve minority dissent in the final result.
10. Return recommendation, conditions, missing evidence, and escalation requirement.

## Rules

- No naive majority voting.
- Proposal author must not act as final judge.
- Security veto cannot be overridden by consensus.
- A debate ends on budget, blocker, insufficient evidence, or protocol stop condition.
- Deliberation recommends; AgenticOS policy and human approval retain execution authority.

## Output

A `debate_result` conforming to `schemas/debate.schema.json`.
