---
name: feature-specification
description: Turn a validated product problem into a scoped, testable implementation specification.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.1"
  category: product
---

# Feature Specification

## Purpose

Translate an evidence-backed product problem into a specification that product, design and engineering can implement and verify.

## Workflow

1. Restate the validated problem and target users.
2. Define desired outcomes and non-goals before detailing behavior.
3. Specify user flows, functional behavior and important edge cases.
4. Define data, integration, security and operational constraints only when supported by context.
5. Write observable acceptance criteria.
6. Identify dependencies, rollout considerations and failure modes.
7. Record unresolved questions instead of silently inventing decisions.

## Guardrails

- Do not expand scope beyond the validated problem without labeling it.
- Do not invent APIs, database fields or infrastructure constraints.
- Acceptance criteria must describe observable behavior, not implementation preference.
- Keep non-goals explicit to control scope creep.
- In a governed composition, do not accept a Skill-to-Skill discovery handoff with an undeclared schema or a data class outside the input contract.

## Output

A structured feature specification with context, scope, flows, requirements, acceptance criteria, risks, dependencies, non-goals and open questions. `skill.yaml` declares the typed `product.discovery-result.v1` input and `product.feature-specification.v1` output used by the composer.
