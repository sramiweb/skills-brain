---
name: lead-qualification
description: Qualify B2B leads against explicit ICP criteria without inventing missing prospect facts.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: sales
---

# Lead Qualification

## Purpose

Decide whether a B2B lead matches a defined ideal customer profile using traceable evidence and explicit uncertainty.

## Workflow

1. Convert the ICP into observable qualification and disqualification criteria.
2. Map each available lead fact to a criterion and preserve its source/freshness when supplied.
3. Separate verified facts, weak signals and unknowns.
4. Score or classify only criteria supported by evidence.
5. Apply explicit disqualifiers before optimistic scoring.
6. Return confidence and the smallest set of missing facts that could change the decision.
7. Keep outreach recommendations separate from the qualification decision.

## Guardrails

- Do not infer company size, budget, authority or intent without evidence.
- Missing data is not a positive signal.
- Do not use protected personal characteristics as qualification criteria.
- Do not contact, enrich or modify external systems; those actions require runtime tools and policy.

## Output

Qualification status, criterion-by-criterion evidence, disqualifiers, confidence, missing information and recommended next verification step.
