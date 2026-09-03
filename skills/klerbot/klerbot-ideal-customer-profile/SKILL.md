---
name: klerbot-ideal-customer-profile
description: Use when a Klerbot mission needs the current buyer/user profile, fit signals, disqualifiers, or ICP assumptions. Do not use as generic lead-scoring methodology and do not present product positioning as validated market research.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: klerbot
---

# Klerbot Ideal Customer Profile

## Purpose

Provide an evidence-qualified Klerbot ICP context so sales, growth, product and market Skills use the same buyer/user model while preserving the difference between verified product facts, product-positioned pain hypotheses and genuinely validated customer evidence.

## Verified role model

- **Primary paying organization:** Moroccan accounting firm / fiduciary.
- **Operational users:** accountants and accounting-team collaborators working across client dossiers.
- **Indirect/end users:** artisans and TPE/PME contacts who submit documents, notably through WhatsApp or direct upload flows.
- **Operator:** Klerbot Super Admin.

This role model comes from the current product design. It does not prove market size, willingness to pay or segment conversion.

## Current fit hypotheses

The current product positioning suggests stronger fit when an accounting firm experiences several of these conditions:

- client documents arrive through multiple channels and formats and require centralization;
- collaborators repeatedly re-enter supplier, ICE, date, HT, TVA, TTC or related accounting fields;
- the team wants inconsistencies such as ICE/TVA or arithmetic issues surfaced before validation/export;
- the firm manages multiple client dossiers and needs a structured review flow;
- the firm values human validation while automating preparation work;
- supported accounting exports can fit its downstream workflow.

Treat these as **ICP hypotheses derived from current product positioning** until backed by customer, pipeline, win/loss, usage or revenue evidence.

## Fit signals to collect

For a real prospect or segment, collect evidence for:

1. Organization type and location.
2. Number and type of client dossiers handled.
3. Monthly document volume and intake channels.
4. Current amount of manual re-entry and anomaly checking.
5. Current accounting/export tools and required formats.
6. Decision maker, operational champions and blockers.
7. Security, data-handling and procurement constraints.
8. Evidence of urgency: backlog, errors, staffing pressure, client-friction or close-period workload.

Do not hard-code minimum employee count, revenue, document volume or software stack unless current evidence supports a threshold.

## Disqualifiers / weak-fit signals

Flag rather than force-fit when:

- the organization is not an accounting/fiduciary buyer and no supported buyer use case is demonstrated;
- the workflow requires capabilities Klerbot does not currently evidence;
- required integrations/export formats are unsupported or unverified;
- the prospect demands fully autonomous accounting with no human validation when the product workflow requires control;
- security, residency or compliance requirements cannot be evidenced as satisfied.

An artisan can be an important product user without being the primary paying ICP.

## Evidence levels

Every ICP statement should be labeled as one of:

- `verified_product_role` — directly supported by current product architecture/content;
- `positioning_hypothesis` — implied by current messaging/problem framing;
- `customer_evidence` — supported by actual prospect/customer/pipeline/usage evidence supplied to the mission;
- `unknown` — not supported yet.

## Composition

Use this context with the generic Skill that performs the job, for example:

- `sales-lead-qualification` / capability `sales.lead.qualify` + this Skill;
- competitor or market analysis + this Skill;
- growth-funnel analysis + this Skill;
- product discovery + this Skill.

## Guardrails

- Do not invent company-size thresholds, revenue bands, conversion rates, willingness to pay or geographic coverage.
- Do not turn landing-page pains into claims that all Moroccan accounting firms share them.
- Do not treat a user persona as a paying buyer without evidence.
- Do not make an outreach or sales decision solely from this context; use a lead-qualification method and real prospect evidence.
- Fresher customer or product evidence overrides this snapshot and should trigger a reported drift when material.

## Output

An ICP brief containing buyer/user roles, evidence-qualified fit hypotheses, observed prospect signals, disqualifiers, unknowns, evidence level for each important claim and the generic Skill to use next.