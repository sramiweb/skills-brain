---
name: klerbot-market-context
description: Use when a Klerbot mission needs durable market positioning, comparison axes, or market assumptions. Do not use as a live competitor database and do not invent market size, regulation, pricing, or competitor features.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: klerbot
---

# Klerbot Market Context

## Purpose

Provide durable Klerbot market-positioning context while keeping time-sensitive market facts, competitor claims and pricing research outside the snapshot. The Skill tells a market-analysis method what Klerbot is trying to differentiate on; it does not replace fresh research.

## Verified positioning

Current product evidence positions Klerbot as:

- an assistant for pre-accounting workflows used by Moroccan accounting firms / fiduciaries and their client ecosystem;
- a document-intake and preparation workflow centered on familiar channels such as WhatsApp and direct upload;
- more than generic OCR: extraction is combined with accounting-oriented consistency checks, anomaly surfacing, human validation and downstream export preparation;
- explicitly human-in-control: AI prepares and proposes, the accounting team validates;
- locally framed around Moroccan accounting data and workflows such as ICE, TVA, MAD and fiduciary/client dossier operations.

These are product-positioning facts. They do not prove competitive superiority or market demand by themselves.

## Durable comparison axes

When fresh competitor or product research is performed, compare evidence on axes that matter to Klerbot rather than using generic feature-counting:

1. **Document intake fit** — WhatsApp, direct upload, PDF/photo/scan and operational friction for the client.
2. **Accounting specificity** — extraction of relevant accounting fields and local consistency controls.
3. **Human control** — review, correction, anomaly handling and auditability before export/action.
4. **Multi-client workflow** — ability to organize accounting-firm client dossiers and team operations.
5. **Downstream interoperability** — verified export/integration formats and configuration effort.
6. **AI architecture** — provider flexibility, failure handling and transparency where evidence is available.
7. **Security / data governance** — only evidenced controls, certifications, hosting/residency and access boundaries.
8. **Commercial fit** — verified pricing model, onboarding burden, support and total workflow cost.

## Market categories to investigate

A live market scan may need to include several substitute categories, not only products branded as "AI accounting":

- document/OCR and invoice-extraction tools;
- accounting/pre-accounting software and ERP/accounting suites;
- client document-collection portals;
- WhatsApp-first or conversational business workflows;
- manual or semi-manual accounting-firm processes that remain the status quo.

This is a research frame, not a claim that named competitors exist in each category or that Klerbot wins against them.

## Evidence discipline

For each market statement, label it as:

- `verified_klerbot_positioning`;
- `fresh_external_evidence`;
- `customer_or_pipeline_evidence`;
- `hypothesis`;
- `unknown`.

Always record the observation date for time-sensitive external evidence.

## Composition

Use this context with generic market Skills such as competitor analysis/monitoring, product landscape scanning or pricing analysis. The generic Skill gathers fresh evidence; this Skill supplies Klerbot-relevant comparison axes and positioning constraints.

## Guardrails

- Do not store a static list of competitors as evergreen truth.
- Do not invent competitor features, prices, funding, customer counts or market share.
- Do not invent Moroccan market size, regulations or tax requirements.
- Do not convert Klerbot marketing claims into independent market evidence.
- Do not say Klerbot is "better", "cheaper", "more secure" or "more compliant" without a current comparison backed by evidence.
- If external evidence changes materially, report drift rather than silently rewriting this context.

## Output

A Klerbot market-context brief containing verified positioning, relevant comparison axes, substitute categories, evidence labels, unknowns and the fresh-research Skill required next.