---
name: product-discovery
description: Discover product problems and opportunities from evidence before proposing features.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.1"
  category: product
---

# Product Discovery

## Purpose

Turn customer, usage and business evidence into clear product problems and opportunity hypotheses without jumping directly to a preferred solution.

## Workflow

1. Separate observed evidence from interpretation and assumptions.
2. Group evidence by user segment, job, friction and business impact.
3. Write problem statements describing who is affected, what happens and why it matters.
4. Estimate evidence strength, recurrence and urgency.
5. Identify opportunity hypotheses without committing to implementation.
6. Surface contradictions and missing evidence that should be researched next.
7. Produce discovery questions that can invalidate the leading hypothesis.

## Guardrails

- Do not convert a single anecdote into a market-wide conclusion.
- Do not treat requested features as validated problems.
- Do not invent customer pain, usage frequency or commercial impact.
- Keep solution ideas separate from problem evidence.

## Output

A prioritized set of problem statements, supporting evidence, confidence, opportunity hypotheses and unresolved discovery questions. When used in a governed composition, this may be handed off through the typed `product.discovery-result.v1` contract declared in `skill.yaml`.
