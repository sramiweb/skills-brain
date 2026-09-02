---
name: subscription-analysis
description: Analyze subscription movements and recurring-revenue structure from explicit billing evidence.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: revenue
---

# Subscription Analysis

## Purpose

Explain subscription changes and plan economics using traceable billing records rather than inferred customer intent.

## Workflow

1. Define the analysis period, currency and subscription-state semantics.
2. Normalize active, new, upgraded, downgraded, cancelled and reactivated subscriptions.
3. Reconcile subscription counts with recurring-revenue movements.
4. Analyze plan mix, concentration and transitions between plans.
5. Detect impossible transitions, missing prices, duplicated subscriptions and inconsistent dates.
6. Separate observed movements from hypotheses about customer motivation.
7. Report data coverage and reconciliation gaps.

## Guardrails

- Do not treat invoices, subscriptions and cash receipts as interchangeable concepts.
- Do not infer churn reasons from cancellation alone.
- Do not mix currencies without an explicit conversion basis.
- Reconciliation failures must be visible, not silently absorbed.

## Output

Subscription movement tables, plan-mix findings, recurring-revenue implications, anomalies, reconciliation status and unresolved data gaps.
