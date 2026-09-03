---
name: klerbot-code-conventions
description: Use when implementing or reviewing Klerbot code and repository changes against project-specific coding, validation, security and quality conventions. Do not use as a generic code-review method.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: klerbot
---

# Klerbot Code Conventions

## Purpose

Provide Klerbot-specific implementation constraints that generic engineering Skills can apply when generating, reviewing or validating changes in the product repository.

## Source-of-truth conventions

### Shared domain model

- Reuse types from `packages/types/src/index.ts`; do not redefine an existing domain interface locally.
- Use type-only imports for shared TypeScript types where applicable.
- Avoid `any`; when an unavoidable boundary requires it, justify the exception in code.
- Treat `packages/db/schema.sql` as the database-schema source of truth.

### Backend

- Validate external inputs with Zod before business processing.
- The WhatsApp webhook acknowledges quickly and delegates expensive work to BullMQ.
- Never perform synchronous AI extraction in the webhook request path.
- Use the existing Supabase client/helpers rather than creating ad-hoc clients.
- Route AI-provider selection through the Klerbot AI factory; do not instantiate Claude, OpenAI, Gemini or another provider directly from feature code.
- Use the project logger for production errors rather than `console.error()`.
- Administrative actions that change or govern system state must remain auditable.

### Frontend

- Use the shared API layer instead of direct ad-hoc `fetch` calls from components.
- Use TanStack Query for server-state fetching and mutations.
- Mutations must surface errors to the user and invalidate the relevant cached query state after successful changes.
- Keep browser code free of backend service credentials and AI-provider secrets.
- Reuse the established component system before adding parallel UI primitives.

### Security and storage

- Never expose the Supabase service key in browser code.
- Never expose private AI-provider credentials in browser code.
- Preserve RLS as an authorization boundary.
- Persist Supabase Storage object paths, not expiring signed URLs.

## Review workflow

1. Determine whether the change touches shared types, DB schema, API, worker/queue, AI, frontend, storage or admin operations.
2. Apply the relevant Klerbot conventions above.
3. Distinguish hard convention violations from optional style improvements.
4. For each violation, identify the exact invariant at risk and the smallest compliant correction.
5. Defer generic code-quality reasoning to `code-review`, `static-analysis`, `security-audit`, `test-strategy` or `regression-testing` as appropriate.
6. Verify the project quality chain after implementation: formatting, lint, type checking and tests. Do not bypass failures merely to make CI green.

## Guardrails

- Do not invent repository conventions that are not evidenced by the Klerbot codebase or its maintained engineering guidance.
- Do not duplicate generic code-review heuristics here.
- Do not convert a convention into a runtime permission.
- When current repository evidence contradicts this snapshot, prefer the repository and report the drift.

## Output

A Klerbot convention report containing applicable rules, concrete violations, severity, minimal remediation and any generic engineering Skill that should perform deeper analysis.