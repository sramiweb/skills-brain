---
name: skill-creator
description: Use this skill when the user wants to create, scaffold, scope, refactor, or extend an Agent Skill (SKILL.md). Triggers on "cré«« un skill", "nouveau skill", "skill pour", "comment structurer ce skill", "create a skill", "scaffold a skill". Do NOT use this skill to execute an existing skill's task, to review non-skill code, or to perform the domain task a skill describes.
license: MIT
compatibility: opencode, claude-code, codex, cursor
metadata:
  author: S R
  version: "1.4.0"
  category: meta
---

# Skill Creator

## Purpose

Governs the full lifecycle of an Agent Skill: scoping a new one, refactoring an existing one, or extending one to cover a related trigger.

## Hard rules

1. **One skill = one job.** Split only if (a) independently invocable AND (b) requires non-trivial guidance.
2. **Duplicate detection:** same triggers + same responsibility (not file format).
3. Frontmatter: only `name`, `description`, `license`, `compatibility`, `metadata`.
4. **Negative scope mandatory** in description.
5. Target <200 lines; externalize to `references/` if longer.
6. **3 scenarios required:** Input, Expected, Actual, Status, Level (L1/L2).

## Workflow

1. Platform → locations → discover → compare → decide (CREATE/EXTEND/REFACTOR/SPLIT)
2. Scope interrogation (task, triggers, negative scope, tools/stack)
3. Frontmatter generation
4. Body structure (Purpose → When → Workflow → Rules → Examples → References)
5. Validation checklist
6. Output (write or content-only)

## Examples

### Happy path
- **Input:** "Cre un skill Zabbix pour diagnostiquer les proxies."
- **Expected:** Platform first, then scope questions
- **Actual:** Correct order, asks about negative scope
- **Status:** PASS · Level: L1

### Edge case
- **Input:** "Amliore cette requte PostgreSQL."
- **Expected:** Does NOT activate
- **Actual:** No activation
- **Status:** PASS · Level: L1

### Stress case
- **Input:** "Cre un skill qui analyse Zabbix, dploie Kubernetes, envoie des emails et gnre des factures."
- **Expected:** Proposes split into 3-4 skills
- **Actual:** 3 skills + email flagged for clarification
- **Status:** PASS · Level: L1
