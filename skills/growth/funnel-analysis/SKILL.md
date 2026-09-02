---
name: funnel-analysis
description: Analyze funnel conversion and drop-off using explicit stages, denominators and cohorts.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: growth
---

# Funnel Analysis

## Purpose

Measure and explain conversion through a defined funnel without hiding denominator changes or instrumentation gaps.

## Workflow

1. Define stage events, ordering rules, cohort entry and analysis window.
2. Validate event coverage, uniqueness and timestamp consistency.
3. Calculate stage-to-stage and overall conversion using explicit denominators.
4. Segment only when sample sizes and definitions remain comparable.
5. Identify drop-offs, delays and abnormal transitions.
6. Separate product behavior from tracking defects and missing events.
7. Rank investigation areas by potential impact and evidence strength.

## Guardrails

- Never compare conversion rates with different denominator definitions without flagging it.
- Do not attribute causality from funnel correlation alone.
- Do not hide missing events or broken instrumentation.
- Avoid over-interpreting tiny cohorts.

## Output

Funnel definitions, conversion metrics, drop-off analysis, segment findings, instrumentation issues, confidence and recommended investigations.
