---
name: skill-resolver
description: Resolve requested capabilities to eligible Skills by filtering policy constraints before ranking candidates.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.2.0"
  category: core
---

# Skill Resolver

## Purpose

Select the best eligible Skill candidates for requested capabilities without confusing ranking, historical reputation or runtime authorization.

## Resolution Order

1. Validate requested capabilities against the canonical ontology.
2. Discover Skills with capability overlap.
3. Reject lifecycle states not allowed by the request.
4. Reject Skills above the maximum risk.
5. Reject Skills whose required tool capabilities are unavailable.
6. Enforce requested data-class constraints.
7. Enforce declared runtime compatibility when present or explicitly required.
8. Rank only the remaining eligible candidates.
9. Optionally use verified **global** exact-version reputation as a bounded post-eligibility ranking signal.
10. Report full vs partial capability coverage, reputation evidence and missing capabilities.

## Ranking

Base ranking uses capability coverage, verified evaluation score, lifecycle maturity and risk fitness. Ranking must never override an eligibility failure.

When a valid global `reputation_report` is supplied and the report entry:

- matches the exact current Skill version;
- is marked `eligible_for_ranking`;
- contains a non-null verified reputation score;

the reference resolver applies the reputation only as a small bounded refinement of the already eligible candidate score.

Tenant-scoped reputation is deliberately rejected by the canonical resolver. Tenant empirical ranking remains a local AgenticOS/runtime concern.

## Guardrails

- Resolution is advisory and returns `authorization: not_granted`.
- A high evaluation or reputation score cannot compensate for missing tools, excess risk, denied lifecycle state, incompatible data class or runtime incompatibility.
- `quarantined` Skills are never eligible.
- Unknown capabilities fail closed rather than being guessed.
- Missing evaluation evidence contributes zero quality rather than an invented score.
- Reputation from an old Skill version is visible as historical evidence but does not score the new version.
- Low-sample or unverified reputation is never converted into ranking confidence.
- Tenant-specific reputation must remain runtime-local and cannot contaminate canonical global ranking.
- Tenant authorization and concrete MCP/tool policy remain AgenticOS responsibilities.

## Output

An ordered candidate list with capability coverage, evaluation quality, optional verified reputation score/sample count, risk, required tools and rejection reasons when explanation is requested.

See `standards/resolution.md` and `standards/reputation.md` for normative behavior.
