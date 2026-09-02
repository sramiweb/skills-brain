---
name: codebase-analysis
description: Analyze repository structure, conventions, dependencies and change surface before implementation.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.1"
  category: engineering
---

# Codebase Analysis

## Purpose

Understand how a codebase actually works before proposing changes, with explicit evidence for architecture, conventions and dependency claims.

## Workflow

1. Identify entry points, major modules, configuration and test structure.
2. Trace the specific execution or data path relevant to the analysis question.
3. Identify internal and external dependencies that constrain the change surface.
4. Extract repository conventions from actual neighboring code rather than generic preferences.
5. Prefer executable implementation and tests over stale documentation when they conflict, while recording the contradiction explicitly.
6. Separate observed architecture from inferred intent.
7. Identify files likely to change, files that should remain untouched and regression-sensitive boundaries.
8. Return missing context instead of inventing unseen implementation details.

## Evidence discipline

Classify important claims as one of:

- **observed** — directly supported by a visible file, dependency, configuration or test;
- **inferred** — reasonable interpretation that is not directly proven;
- **unresolved** — required information is not present in the visible repository scope.

For change-surface analysis, state why each file is included and avoid widening the surface without evidence.

## Guardrails

- Do not infer unseen file contents.
- Do not recommend a rewrite before understanding local conventions and constraints.
- Do not treat README claims as stronger evidence than actual implementation when they conflict.
- Do not silently fetch external context to fill repository gaps.
- This Skill is read-only and must not modify repository files.
- Do not request filesystem write, shell execution or network access as a convenience for canonical analysis.

## Output

A codebase map focused on the requested problem, including:

- relevant entry points and execution/data paths;
- evidence-backed internal/external dependencies;
- repository conventions relevant to the question;
- contradictions between documentation and implementation;
- likely change surface and likely untouched boundaries;
- regression-sensitive tests or contracts;
- observed facts, inferences and unresolved questions clearly separated.
