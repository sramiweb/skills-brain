---
name: klerbot-product-context
description: Use when a Klerbot mission needs verified product, user, business-model, or workflow context. Do not use for generic product discovery or for tasks unrelated to Klerbot.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: klerbot
---

# Klerbot Product Context

## Purpose

Provide a compact, evidence-oriented product context for Klerbot so product, customer, revenue, content, sales and engineering Skills reason about the same product instead of inventing their own version of it.

## Verified product model

- Klerbot is a WhatsApp accounting assistant for Moroccan TPEs and artisans.
- The commercial model is B2B2C: accounting firms / fiduciaries are the paying customers, artisans use WhatsApp with minimal friction, and a Super Admin operates the platform.
- The core flow is: invoice photo on WhatsApp → Meta webhook → authorized-number check → BullMQ job → AI extraction → arithmetic / duplicate validation → Supabase persistence → WhatsApp confirmation → accountant dashboard.
- The accountant experience centers on companies, extracted documents, anomalies, exports, subscription and settings.
- The Super Admin experience includes operational monitoring, queue supervision, AI-provider supervision, fiduciary management, provisioning, logs and configuration.

## How to use this context

1. Identify which Klerbot user is affected: fiduciary/accountant, artisan, or Super Admin.
2. Separate current verified behavior from a requested change or hypothesis.
3. Map the mission to the existing product flow before proposing a new surface or service.
4. State any missing evidence instead of filling gaps with plausible SaaS behavior.
5. Hand the verified context to the generic Skill responsible for the actual job, for example `product-discovery`, `feature-specification`, `roadmap-prioritization`, `customer-health-analysis` or `saas-metrics-analysis`.

## Guardrails

- Do not invent features, pricing, customer counts, revenue, conversion, retention, legal status or roadmap commitments.
- Do not turn this context Skill into a product-management methodology; reusable methods stay generic.
- Do not treat a proposed capability as already shipped.
- Do not infer tenant runtime permissions, connectors or credentials from product context.
- When current repository or runtime evidence contradicts this snapshot, prefer the fresher evidence and report the drift.

## Output

A short Klerbot context brief containing the relevant user, verified current behavior, product constraints, explicitly unknown facts and the generic Skill that should perform the requested analysis or creation task.