---
name: skill-resolver
description: Resolve requested capabilities to eligible Skills by filtering policy constraints before ranking candidates.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: core
---

# Skill Resolver

## Purpose

Select the best eligible Skill candidates for requested capabilities without confusing ranking with runtime authorization.

## Resolution Order

1. Validate requested capabilities against the canonical ontology.
2. Discover Skills with capability overlap.
3. Reject lifecycle states not allowed by the request.
4. Reject Skills above the maximum risk.
5. Reject Skills whose required tool capabilities are unavailable.
6. Enforce requested data-class constraints.
7. Enforce declared runtime compatibility when present or explicitly required.
8. Rank only the remaining eligible candidates.
9. Report full vs partial capability coverage and missing capabilities.

## Ranking

Ranking may use capability coverage, verified evaluation score, lifecycle maturity and risk fitness. Ranking must never override an eligibility failure.

## Guardrails

- Resolution is advisory and returns `authorization: not_granted`.
- A high quality score cannot compensate for missing tools or incompatible data classes.
- `quarantined` Skills are never eligible.
- Unknown capabilities fail closed rather than being guessed.
- Missing evaluation evidence contributes zero quality rather than an invented score.
- Tenant authorization and concrete MCP/tool policy remain AgenticOS responsibilities.

## Output

An ordered candidate list with coverage, quality evidence, risk, required tools and rejection reasons when explanation is requested.
