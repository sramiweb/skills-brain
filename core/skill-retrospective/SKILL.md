---
name: skill-retrospective
description: Convert verified outcomes into scoped learning candidates and controlled Skill improvement proposals.
license: MIT
compatibility: skills-brain, agenticos
metadata:
  author: sramiweb
  version: "1.0.0"
  category: core
---

# Skill Retrospective

## Purpose

Turn execution outcomes into evidence-backed learning without allowing uncontrolled self-modification.

## Workflow

1. Compare expected outcome with observed outcome.
2. Identify what worked, failed, was unnecessary, or depended on a wrong assumption.
3. Record the observation as a signal.
4. Search for repeated related signals within the same scope.
5. Promote repeated evidence to a pattern, then to a hypothesis only when justified.
6. Require an experiment or verified outcome before marking a learning as verified.
7. Decide whether the learning is tenant-specific or reusable.
8. For reusable learning, produce an `improvement_proposal` targeting a Skill or protocol.
9. Require tests, evaluation, review/deliberation and approval before a new Skill version is promoted.

## Rules

- One observation is a signal, not knowledge.
- Memory is historical context, not current truth.
- New contradictory evidence reduces confidence and can trigger revalidation.
- Never modify production code, policy, permissions, or a canonical Skill directly from a retrospective.
- Cross-tenant promotion requires explicit generalization review.

## Output

A scoped learning candidate plus, when justified, an improvement proposal conforming to the Skills Brain schemas.
