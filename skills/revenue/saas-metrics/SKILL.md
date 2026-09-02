---
name: saas-metrics
description: Calculate SaaS metrics from normalized source data with explicit formulas, period boundaries and data-quality warnings.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: revenue
---

# SaaS Metrics

## Purpose

Calculate standard SaaS business metrics without hiding assumptions or mixing incompatible periods.

## Metrics

Depending on available data, calculate and explain:

- MRR and ARR.
- New, expansion, contraction and churned MRR.
- Logo and revenue churn.
- ARPU/ARPA.
- Trial-to-paid conversion.
- Revenue by plan/cohort.
- Retention and lifetime indicators.
- Unit-economics inputs when cost data is supplied.

## Workflow

1. Validate reporting period, currency and subscription states.
2. Normalize recurring revenue and exclude one-off amounts when the metric requires recurring revenue only.
3. Calculate each metric from a documented formula.
4. Reconcile totals where possible.
5. Report missing, duplicated or contradictory billing records.
6. Compare periods/cohorts only when definitions are consistent.

## Guardrails

- Never invent CAC, LTV or margin when required inputs are absent.
- Never modify billing, pricing or subscription state.
- State whether results are exact, estimated or incomplete.
- Do not mix monthly and annual amounts without normalization.
