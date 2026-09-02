---
name: roadmap-prioritization
description: Prioritize roadmap candidates from evidence and explicit scoring dimensions; recommendation only, never final approval.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: product
---

# Roadmap Prioritization

## Purpose

Turn a set of product opportunities into an explainable roadmap recommendation without confusing scoring with the final decision.

## Workflow

1. Reject candidates with no identifiable problem or supporting evidence.
2. Normalize evidence strength and freshness.
3. Score customer impact, business/revenue impact, strategic fit, competitive urgency, risk reduction, confidence and engineering effort.
4. Surface dependencies and mutually exclusive candidates.
5. Produce a ranked shortlist plus reasons, not only numbers.
6. Flag high-impact or disputed candidates for strategic debate.
7. Preserve rejected/deferred candidates and the reason for the decision.

## Default scoring dimensions

Weights are runtime/context configurable; the Skill must not hard-code them as universal truth.

- Customer impact.
- Business/revenue impact.
- Strategic fit.
- Evidence strength.
- Competitive urgency.
- Reliability/security impact.
- Confidence.
- Effort/dependencies.

## Guardrails

- No roadmap item without evidence.
- A high score does not bypass security, feasibility or human approval.
- Do not reward false precision when evidence is weak.
- Preserve dissent from Engineering, Customer, Revenue or Security reviews.
