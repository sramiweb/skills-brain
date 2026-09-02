---
name: competitor-analysis
description: Compare competitors using fresh, traceable evidence and fixed criteria without inventing claims.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: market
---

# Competitor Analysis

## Purpose

Compare competitors or alternative products using evidence that can be traced, dated and challenged.

## Workflow

1. Define the comparison question and fixed criteria before scoring competitors.
2. Normalize evidence by competitor, source and observation date.
3. Separate facts, interpretations and unknowns.
4. Compare target customers, positioning, pricing, features, integrations and distribution only when evidence exists.
5. Detect material gaps, strengths, weaknesses and changes.
6. Assess potential impact on the subject product without turning speculation into fact.
7. Return missing evidence and confidence per conclusion.

## Guardrails

- Do not compare a current price with stale competitor data without flagging freshness.
- Do not infer market share from social visibility alone.
- Do not invent features, customers or pricing.
- Prefer `insufficient_evidence` over false precision.

## Output

A structured comparison with evidence references, observed differences, implications, confidence and unresolved questions.
