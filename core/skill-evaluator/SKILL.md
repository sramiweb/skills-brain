---
name: skill-evaluator
description: Evaluate a Skills Brain candidate using Q0-Q5 gates and execution evidence without fabricating PASS results.
license: MIT
compatibility: skills-brain, agenticos
metadata:
  author: sramiweb
  version: "1.0.0"
  category: core
---

# Skill Evaluator

## Purpose

Assess whether a Skill is eligible for promotion by applying the canonical Q0-Q5 evaluation model.

## Workflow

1. Validate the canonical manifest and SKILL.md contract (Q0).
2. Check static quality, permissions, declared side effects and risk consistency (Q1).
3. Validate scenario definitions and negative cases (Q2).
4. Validate security-policy test definitions and sandbox evidence when required (Q3).
5. Require externally generated, verified Golden Task results for Q4.
6. Require verified regression evidence for Q5 when policy requires it.
7. Compare the resulting score with `evaluation.minimum_score`.
8. Return a structured verdict: `pass`, `retest`, `reject`, or `quarantine`.

## Rules

- Never convert a manually authored expectation into execution evidence.
- Never mark a missing Q4/Q5 result as PASS.
- High-risk Skills require stronger gates, not weaker ones.
- Evaluation does not activate a Skill; lifecycle promotion is a separate governed decision.

## Output

Return gate results, score, missing evidence, critical findings, and promotion recommendation.

## Examples

A risk-4 migration Skill with valid YAML but no verified regression result must remain non-promotable even if its documentation is excellent.
