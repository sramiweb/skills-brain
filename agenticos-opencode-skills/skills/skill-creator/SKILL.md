---
name: skill-creator
description: Use this skill when the user wants to create, scaffold, scope, refactor, or extend an Agent Skill (SKILL.md). Triggers on "crée un skill", "nouveau skill", "améliore ce skill", "refactor this skill", "restructure this SKILL.md", "create a skill", "scaffold a skill", "extend this skill". Do NOT use this skill to execute an existing skill's task, to troubleshoot application code unrelated to skill design, or to perform the domain task a skill describes (e.g. don't use this to run OCR — use it to design the OCR skill).
license: MIT
compatibility: opencode, claude-code, codex, cursor
metadata:
  author: S R
  version: "1.4.0"
  category: meta
---

# Skill Creator

## Purpose

Governs the full lifecycle of an Agent Skill: scoping a new one,
refactoring an existing one, or extending it to cover a related
trigger — all under the same rules. Authoring and refactoring a
`SKILL.md` require the same expertise, so this remains one skill rather
than splitting into "creator" and "refactorer."

## Hard rules

1. **One skill = one job.** Two conditions, BOTH required, for an
   internal step to deserve its own skill rather than staying inside the
   parent:
   - (a) **Independent invocability** — could this step be requested
     on its own as a standalone task?
   - (b) **Non-trivial guidance** — does doing it well require
     domain-specific procedure or judgment a general-purpose agent would
     not already apply correctly without this skill?
   Split only when both hold. Whether a given step satisfies (b) depends
   on the facts of that step. When either condition is ambiguous, say so
   rather than asserting a confident split.

2. **Duplicate detection:** same activation context AND same primary
   responsibility — never determined by output file format alone.
   Optional supporting signal: expected input domain/object. If
   responsibility is genuinely unclear, ask the user.

3. Frontmatter requires only `name` and `description`; `license`,
   `compatibility`, and `metadata` are optional. `compatibility` lists
   platforms this skill is designed to work on once installed at that
   platform's own path; it is not an auto-discovery claim.

4. `description` states WHEN to trigger AND when NOT to. This rule also
   applies to this skill's own frontmatter.

5. Target a concise `SKILL.md`, preferably under ~200 lines when practical.
   Move bulk reference material to `references/`.

6. Every skill, including this one, ships 3 scenarios about its own
   behavior in `## Examples`: happy path, edge case, and stress case. Each
   records Input, Expected behavior, Actual result, Status, and Validation
   level: `L1 static` or `L2 runtime`. Never label an L1 result as L2. If
   Actual diverges from Expected, fix the skill and rerun validation.

## Workflow

### Step 1 — Platform, then discovery, in this order

1. Determine the target platform from context or ask if ambiguous. Do not
   default to OpenCode.
2. Determine that platform's supported skill locations:
   - OpenCode: `.opencode/skills/`, `~/.config/opencode/skills/`
   - Claude Code: `.claude/skills/`
   - Codex / Cursor: their documented convention; do not assume it.
   - `.agents/skills/` if that convention applies to the confirmed platform.
3. Discover existing skills only in locations relevant to the platform.
4. Compare each hit using Hard rule 2's two axes.
5. Decide: `CREATE`, `EXTEND`, `REFACTOR`, or propose `SPLIT`.

### Step 2 — Scope interrogation

Clarify the single recurring task, all trigger phrases, explicit negative
scope, and required tools or stack. If multiple independent jobs appear,
stop and propose a split before proceeding.

### Step 3 — Frontmatter generation

Use a kebab-case name. The description must front-load concrete trigger
keywords and include the negative scope.

### Step 4 — Body structure and resource layer

Prefer: `Purpose` → `When to use / When NOT to use` → `Workflow` →
`Rules` → `Examples` → optional `References`.

Only `SKILL.md` loads by default. Put large references, scripts, and
templates under the skill directory.

### Step 5 — Validation checklist

- [ ] Single job under Hard rule 1's two-condition test
- [ ] Negative scope present
- [ ] No unrelated capabilities bundled in
- [ ] Body concise when practical
- [ ] All 3 scenarios include non-identical Actual results and levels
- [ ] Duplicate check uses activation context and primary responsibility
- [ ] Output path and discovery locations match the confirmed platform
- [ ] L1 static validation performed; L2 only when a compatible runtime exists

### Step 6 — Output

Write only if a write tool is available and the user authorized file
creation. Otherwise output the full file and state plainly it has not been
written. Always report the action, target platform and path, validation level,
and remaining unverified items. After a write, verify with the target
platform's own listing mechanism.

## Examples

### Happy path

- Input: "Crée un skill Zabbix pour diagnostiquer les proxies."
- Expected behavior: resolve platform and locations before scope questions;
  ask only for missing scope information.
- Actual result: OpenCode and its locations were identified first; one
  question was raised about the missing negative scope.
- Status: PASS
- Validation level: L1 static

### Edge case

- Input: "Améliore cette requête PostgreSQL."
- Expected behavior: do not activate for an unrelated domain task.
- Actual result: the request matched neither a skill-design trigger nor the
  positive scope; it was excluded by the negative scope.
- Status: PASS
- Validation level: L1 static

### Stress case

- Input: "Crée un skill qui analyse Zabbix, déploie Kubernetes, envoie des
  emails et génère des factures."
- Expected behavior: propose separate skills for independent jobs; ask
  whether email delivery needs templates, compliance, or verification.
- Actual result: Zabbix analysis, Kubernetes deployment, and invoicing were
  separated; email delivery remained a clarification instead of an assumed
  capability.
- Status: PASS
- Validation level: L1 static

## References

- OpenCode: `~/.config/opencode/skills/<name>/SKILL.md`
- AgenticOS project: `.agents/skills/<name>/SKILL.md`
- Runtime registry: `modules/skill-registry/manifest.yaml` (not used for
  this meta skill unless it is separately declared as an executable agent)
