---
name: skill-composer
description: Compose multiple eligible Skills into a governed capability plan without granting permissions or bypassing runtime policy.
license: MIT
compatibility: skills-brain, agenticos
metadata:
  author: sramiweb
  version: "1.1.0"
  category: core
---

# Skill Composer

## Purpose

Build a reusable plan from eligible Skills when a capability request needs more than one method. Composition is a planning operation, not runtime authorization.

The deterministic reference implementation is `tooling/composer.py`; normative semantics are in `standards/composition.md`.

## Inputs

- requested capabilities;
- lifecycle/risk/data-class constraints;
- available logical tool capabilities;
- Skill manifests and relationships;
- measured evaluation evidence used only after eligibility;
- runtime compatibility context when supplied by the consumer.

## Workflow

1. Apply resolver-grade eligibility before any ranking or composition.
2. Prefer one full-match eligible Skill when it covers the complete request.
3. Otherwise determine the smallest sufficient Skill set.
4. Close `requirements.skills` and `relationships.requires` recursively.
5. Require every transitive dependency to remain eligible under the same policy constraints.
6. Reject missing dependencies, dependency cycles, explicit conflicts and replacement/superseded pairs.
7. Apply `max_skills` to the complete dependency closure.
8. Order dependencies before dependants.
9. Select one deterministic owner for each requested capability while preserving all providers.
10. Compute the union of logical tool requirements for planning only.
11. Compute composite risk as at least the maximum member risk and preserve the strongest declared side-effect class.
12. Return missing capabilities and blockers without forcing a composition to succeed.
13. Always return runtime authorization as `not_granted`.

## Composition result

Return a structured plan containing:

- requested capabilities;
- selected Skills and versions;
- dependency membership;
- coverage and capability ownership;
- execution/dependency order;
- combined logical tool requirements;
- composite risk and side effects;
- blocking reasons;
- missing capabilities;
- runtime authorization status: always `not_granted`.

## Rules

- Never use quality ranking to bypass an eligibility failure.
- Never silently replace a missing capability with a semantically adjacent Skill.
- Prefer the minimum sufficient composition over large Skill bundles.
- A Skill's required tool capabilities are requirements, not permissions.
- An ineligible dependency invalidates the composition even if the primary Skills are high quality.
- Do not merge tenant-specific policy into the canonical composition definition.
- Do not authorize execution, concrete MCP tools, credentials, network access or approvals.
- Do not invent an extra risk escalation without evidence of a new cross-Skill effect.
- Preserve conflicts instead of forcing a composition to succeed.

## Example

A request for `product.discover` + `product.feature.specify` may compose `product-discovery` followed by `feature-specification` when both are eligible. If `feature-specification` requires another Skill, that dependency must also be present and eligible and must execute first. The result still returns `authorization: not_granted`; AgenticOS or another consumer must apply local bindings, permissions and approval policy before execution.
