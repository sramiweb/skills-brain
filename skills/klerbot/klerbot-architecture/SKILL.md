---
name: klerbot-architecture
description: Use when a Klerbot mission needs the current product architecture, service boundaries, data flow, or technical invariants. Do not use as a generic system-design method or as runtime permission.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: klerbot
---

# Klerbot Architecture

## Purpose

Provide the canonical technical context and non-negotiable architecture constraints of Klerbot so engineering and review Skills assess changes against the product that actually exists.

## Current architecture snapshot

- Monorepo managed with Turborepo.
- `apps/web`: Next.js 14 App Router + React 18 + TanStack Query.
- `apps/api`: Node.js + Express with BullMQ workers.
- Redis backs the asynchronous job queue.
- Supabase provides PostgreSQL, Auth, Storage and Row Level Security.
- AI extraction is multi-provider and must flow through the Klerbot AI factory rather than direct provider calls.
- WhatsApp integration uses the Meta Cloud API.
- Stripe is the payment provider.
- Production packaging uses Docker Compose behind Traefik v3.

## Critical flow invariants

1. The WhatsApp webhook must acknowledge quickly with HTTP 200 before expensive asynchronous processing.
2. Incoming WhatsApp authenticity is validated from the raw request body before JSON parsing.
3. AI/OCR work is queued; it must not block the webhook request path.
4. Backend-only secrets such as the Supabase service key and AI-provider credentials must never cross into browser code.
5. Supabase RLS remains part of the authorization boundary; bypass-capable service credentials stay server-side.
6. Storage records keep the object path and regenerate signed URLs when needed rather than persisting expiring signed URLs.
7. Administrative actions are auditable.
8. Shared TypeScript domain types and the database schema remain canonical sources of truth rather than being redefined in feature code.

## Architecture review workflow

1. Identify the affected layer: web, API, queue/worker, database/storage, AI, WhatsApp, payment or infrastructure.
2. Trace the proposed change through the existing end-to-end data flow.
3. Check whether it crosses an existing trust, async, tenancy or authorization boundary.
4. Prefer extending an existing service boundary over adding a parallel implementation.
5. Flag any change that bypasses the queue, AI factory, shared types, RLS, audit trail or server-only secret boundary.
6. Separate verified current architecture from proposed future architecture.
7. Hand generic architecture trade-off analysis to reusable engineering Skills where appropriate.

## Guardrails

- Do not invent infrastructure components, deployment topology, cloud services or production addresses that are not evidenced.
- Do not encode AgenticOS MCP tools, tenant bindings or approval state in this canonical Skill.
- Do not treat this snapshot as fresher than repository evidence; if the product repo has changed, prefer the repo and report the drift.
- Do not use architecture context to bypass security review or human approval.

## Output

A Klerbot architecture brief containing affected components, current boundaries, violated or preserved invariants, dependencies, risks, unknowns and any recommended generic engineering Skill to apply next.