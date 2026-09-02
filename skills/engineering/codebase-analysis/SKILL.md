---
name: codebase-analysis
description: Analyze repository structure, conventions, dependencies and change surface before implementation.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
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
5. Separate observed architecture from inferred intent.
6. Identify files likely to change, files that should remain untouched and regression-sensitive boundaries.
7. Return missing context instead of inventing unseen implementation details.

## Guardrails

- Do not infer unseen file contents.
- Do not recommend a rewrite before understanding local conventions and constraints.
- Do not treat README claims as stronger evidence than actual implementation when they conflict.
- This Skill is read-only and must not modify repository files.

## Output

A codebase map focused on the requested problem, relevant execution paths, dependencies, conventions, change surface, regression risks and unresolved questions.
