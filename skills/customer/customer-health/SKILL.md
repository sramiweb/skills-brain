---
name: customer-health
description: Assess customer health from observable product and business signals while minimizing personal data exposure.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: customer
---

# Customer Health

## Purpose

Classify customer health using transparent signals rather than intuition. Typical outcomes are `healthy`, `attention`, `at-risk`, `inactive`, or `insufficient-evidence`.

## Workflow

1. Use pseudonymized/aggregated data when identity is unnecessary.
2. Check freshness and completeness of activity, activation, feature adoption, retention, support and billing signals.
3. Apply the supplied health scoring policy; do not invent permanent weights.
4. Explain which signals contributed positively or negatively.
5. Flag missing data and conflicting signals.
6. Recommend a follow-up category, not an unapproved customer contact action.
7. Compare predictions with later churn/retention outcomes to recalibrate the scoring policy.

## Guardrails

- Do not include customer documents, email addresses or identifiers when aggregate signals are sufficient.
- Health score is a decision-support signal, not a fact about customer intent.
- Stale activity must not be treated as current engagement.
- Never contact, downgrade, cancel or modify a customer account from this Skill.
