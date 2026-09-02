---
name: skill-composer
description: Compose multiple eligible Skills into a governed capability plan without granting permissions or bypassing runtime policy.
license: MIT
compatibility: skills-brain, agenticos
metadata:
  author: sramiweb
  version: "1.0.0"
  category: core
---

# Skill Composer

## Purpose

Build a reusable plan from several eligible Skills when one Skill cannot cover the requested capability set. Composition is a planning operation, not runtime authorization.

## Inputs

- requested capabilities;
- resolver candidates and eligibility reasons;
- Skill manifests and relationships;
- compatibility constraints;
- risk ceiling and data-class constraints;
- runtime context supplied by the consumer when available.

## Workflow

1. Start only from Skills already considered eligible by the resolver/policy layer.
2. Determine the smallest Skill set that covers the requested capabilities.
3. Respect declared `requirements.skills`, conflicts, supersedes/extends and compatibility metadata.
4. Order Skills by dependency and information flow.
5. Identify overlapping responsibilities and choose a single owner for each output contract.
6. Calculate the composite risk as at least the maximum member risk, then increase it if composition introduces new cross-Skill effects.
7. Compute required logical tool capabilities as a union for planning only.
8. Explicitly state that runtime permissions remain the intersection of local policies; composition never grants the union automatically.
9. Identify data handoffs and prevent broader data exposure than each participant requires.
10. Surface unresolved conflicts, missing capabilities and approval requirements.

## Composition result

Return a structured plan containing:

- requested capabilities;
- selected Skills and versions;
- coverage map;
- execution/dependency order;
- inputs/outputs between Skills;
- combined logical requirements;
- composite risk and side effects;
- conflicts or incompatibilities;
- missing capabilities;
- runtime authorization status: always `not_granted`;
- recommended review/debate when composition is high-risk or ambiguous.

## Rules

- Never use quality ranking to bypass an eligibility failure.
- Never silently replace a missing capability with a semantically adjacent Skill.
- Prefer the minimum sufficient composition over large Skill bundles.
- A Skill's required tool capabilities are requirements, not permissions.
- Do not merge tenant-specific policy into the canonical composition definition.
- Do not authorize execution, concrete MCP tools, credentials, network access or approvals.
- Preserve conflicts and dissent instead of forcing a composition to succeed.

## Example

A request for `product.discover` + `product.feature.specify` may compose `product-discovery` followed by `feature-specification` only if both are eligible. The output of discovery becomes evidence/input for specification. The composer still returns `authorization: not_granted`; AgenticOS or another consumer must apply local policy before execution.
