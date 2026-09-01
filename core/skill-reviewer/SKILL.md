---
name: skill-reviewer
description: Use this skill when the user wants to audit, review, or refactor an existing Agent Skill (SKILL.md) for compliance with best practices. Triggers on "review this skill", "audit this SKILL.md", "refactor ce skill", "rendre ce skill conforme", "skill review", "skill audit". Do NOT use this skill to create a new skill from scratch (use skill-creator for that), to review non-skill code, or to execute the domain task a skill describes.
license: MIT
compatibility: opencode, claude-code, codex, cursor
metadata:
  author: S R
  version: "1.0.0"
  category: meta
---

# Skill Reviewer

## Purpose

Audits an existing SKILL.md file against the hard rules from skill-creator v1.4.0, identifies gaps, and proposes concrete fixes. This skill does NOT create new skills — it only reviews and refactors existing ones. It is platform-agnostic and works on any project that uses SKILL.md files.

## When to use / When NOT to use

**Use this skill when:**
- A user asks to "review", "audit", "refactor", or "make compliant" an existing SKILL.md
- You need to validate a skill before merging it to a shared repository
- You suspect a skill violates best practices (missing negative scope, no scenarios, etc.)

**Do NOT use this skill for:**
- Creating a new skill from scratch (delegate to skill-creator)
- Reviewing non-skill code (application logic, configs, etc.)
- Executing the domain task described in the skill (e.g., don't run OCR because the skill is about OCR)

## Hard rules (compliance checklist)

### R1 — Scope unique
A skill must have exactly one job. If an internal step could be invoked alone to satisfy a different plausible user request, it's a separate job.
- **CRITICAL** if the skill bundles multiple independent capabilities (e.g., "extract + validate + deploy" without clear dependency chain)
- **Check**: scan for multiple distinct verbs in the Purpose/Workflow that could each be a standalone request

### R2 — Pas de doublon
A skill is a duplicate if it shares BOTH (a) same activation triggers/context AND (b) same primary responsibility with an existing skill.
- **WARNING** if another skill in the same repo has a substantially similar `description` frontmatter
- **Check**: compare `description` field against all other SKILL.md in the same skills directory

### R3 — Frontmatter minimal
Frontmatter must contain only `name`, `description`, `license`, `compatibility`, `metadata`.
- **INFO** if extra fields are present (not blocking, but non-standard)
- **Check**: parse YAML frontmatter, list fields beyond the allowed set

### R4 — Negative scope
The `description` field MUST state when NOT to trigger (negative scope), e.g., "Do NOT use for...".
- **CRITICAL** if missing — the skill cannot reliably auto-activate without this
- **Check**: search for "Do NOT", "Ne pas utiliser", "not for", or equivalent in `description`

### R5 — Conciseness
The SKILL.md body should be under ~200 lines for scanability.
- **WARNING** if body exceeds 200 lines without externalizing bulk to `references/`
- **Check**: count lines in the file (excluding frontmatter)

### R6 — Scenarios
Every skill must have 3 scenarios in `## Examples`: happy path, edge case, stress case, each with Input, Expected behavior, Actual result, Status, Validation level.
- **CRITICAL** if fewer than 3 scenarios, or if any scenario lacks the 5 fields, or if `Actual` merely repeats `Expected`
- **Check**: search for `### Happy path`, `### Edge case`, `### Stress case` subsections and validate field presence

## Workflow

1. **Obtain the SKILL.md content** — read from file attachment, GitHub repo, or pasted content
2. **Parse frontmatter** — extract `name`, `description`, `license`, `compatibility`, `metadata`
3. **Run compliance checklist** against Hard rules R1-R6 above
4. **Classify findings** as CRITICAL (blocks usage), WARNING (should fix), or INFO (optional improvement)
5. **Propose fixes** — for each finding, provide the exact corrected text or structure
6. **Output audit report** — structured summary with severity, location, and fix proposal

## Rules

- Never declare a skill "compliant" without checking all 6 rules explicitly
- If a rule check cannot be completed (e.g., missing context to compare for R2), mark it as UNVERIFIED rather than PASS
- For R6, an `Actual` field that just restates `Expected` is not a valid pass — flag as CRITICAL
- When proposing fixes, always show the exact corrected text, not just a description of the change

## Examples

### Happy path

- **Input:** User attaches `invoice-ocr-extract/SKILL.md` with complete frontmatter, negative scope, 3 scenarios with distinct Actual results
- **Expected behavior:** Returns audit report with all checks PASS, maybe 1-2 INFO suggestions
- **Actual result:** L1 walkthrough confirms structure is valid
- **Status:** PASS
- **Validation level:** L1 static

### Edge case

- **Input:** User pastes a SKILL.md with negative scope missing and only 2 scenarios
- **Expected behavior:** Flags CRITICAL for R4 and R6, proposes exact text to add
- **Actual result:** L1 walkthrough confirms gaps identified
- **Status:** PASS
- **Validation level:** L1 static

### Stress case

- **Input:** User asks to review a 350-line "god skill" that does OCR, validation, email, and deployment
- **Expected behavior:** Flags CRITICAL for R1 (multiple jobs), R5 (too long), R4 (likely missing negative scope), proposes splitting into 3-4 skills
- **Actual result:** L1 walkthrough confirms multi-job violation
- **Status:** PASS
- **Validation level:** L1 static

## References

- skill-creator v1.4.0 (source of truth for Hard rules 1-6)
- skill-template-*.md files (reference structures for compliant skills)
