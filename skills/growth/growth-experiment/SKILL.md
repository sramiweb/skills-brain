---
name: growth-experiment
description: Design measurable growth experiments with explicit hypotheses, metrics and guardrails.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: growth
---

# Growth Experiment

## Purpose

Turn a growth problem into an experiment that can produce a decision rather than just activity.

## Workflow

1. State the observed problem and baseline evidence.
2. Write one falsifiable hypothesis linking intervention, audience and expected behavior.
3. Define primary metric, secondary metrics and guardrails before execution.
4. Specify population, control/comparison strategy and exposure rules.
5. Define minimum observation window and decision/stopping rules.
6. Identify confounders, implementation risks and instrumentation requirements.
7. Define what decision follows positive, negative or inconclusive results.

## Guardrails

- Do not call a tactic an experiment without a falsifiable hypothesis and decision rule.
- Do not change success metrics after observing results without recording the change.
- Guardrail metrics must protect user experience, revenue or operational stability when relevant.
- Execution and external messaging require separate runtime authorization.

## Output

Experiment hypothesis, population, intervention, metrics, guardrails, instrumentation, stopping rules, risks and post-result decision tree.
