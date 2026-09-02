---
name: skill-evaluator
description: Evaluate a Skills Brain candidate using Q0-Q5 gates and independently verified execution evidence without fabricating PASS results.
license: MIT
compatibility: skills-brain, agenticos
metadata:
  author: sramiweb
  version: "1.1.0"
  category: core
---

# Skill Evaluator

## Purpose

Assess whether a Skill is eligible for promotion by applying the canonical Q0-Q5 evaluation model and verifying that Q4/Q5 evidence is current, complete and independently checked.

## Workflow

1. Validate the canonical manifest and `SKILL.md` contract (Q0).
2. Check static quality, logical requirements, declared side effects and risk/security consistency (Q1).
3. Validate scenario definitions and negative cases (Q2).
4. Validate security-policy test definitions and sandbox evidence when required (Q3).
5. For Q4, require a Golden Task result generated through the canonical evaluation harness from external execution plus independent verification.
6. For Q5, require independently verified regression evidence when policy requires it.
7. Recompute the current Skill package hash and evaluation-definition hash; reject stale evidence.
8. Require exact coverage of current task/check IDs and reject duplicate, missing or extra results.
9. Compare the resulting gate score with `evaluation.minimum_score` while preserving mandatory-gate failures.
10. Return a structured verdict: `pass`, `retest`, `reject`, or `quarantine`.

## Q4/Q5 evidence chain

```text
prepare request
  -> external runner
  -> independent verifier
  -> eval_harness finalize
  -> evaluator re-validation
```

The runner and verifier must be different identities. A verified result is bound to Skill ID, version, `package_sha256` and the exact Golden/Regression definition hash.

## Rules

- Never convert a manually authored expectation into execution evidence.
- Never mark missing Q4/Q5 evidence as PASS.
- Never accept a result generated for an older package or older evaluation definition.
- Never allow aggregate score to override a mandatory failed gate.
- High-risk Skills require stronger gates, not weaker ones.
- Evaluation does not activate a Skill; lifecycle promotion is a separate governed decision.
- Runtime authorization remains outside Skills Brain evaluation.

## Output

Return gate results, score, missing/stale evidence, critical findings and promotion recommendation.

## Examples

A risk-4 migration Skill with valid YAML but no verified regression result must remain non-promotable even if its documentation is excellent.

A Skill with a previously passing Golden Task must be re-evaluated if `SKILL.md`, `skill.yaml`, a source asset or `golden.yaml` changes, because the previous result no longer matches the current package identity.
