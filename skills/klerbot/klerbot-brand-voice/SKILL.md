---
name: klerbot-brand-voice
description: Use when Klerbot marketing, onboarding, product or sales copy must sound consistent with the product's current voice and claims. Do not use as a generic writing Skill or to invent unsupported product/security claims.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: klerbot
---

# Klerbot Brand Voice

## Purpose

Provide Klerbot-specific voice, framing and claim discipline so reusable writing Skills produce copy that feels consistent with the current product without fabricating capabilities or guarantees.

## Audience

Primary business audience:
- Moroccan fiduciaries and accounting firms.
- TPE / PME operators evaluating a simpler document-collection and pre-accounting workflow.

End-user context:
- Artisans can submit invoices through familiar channels such as WhatsApp with minimal operational friction.

## Voice characteristics

- **Clear before clever**: explain the workflow in concrete steps and familiar accounting terms.
- **Practical and operational**: favor outcomes such as centralizing documents, extracting fields, checking ICE/TVA consistency and preparing exports.
- **Reassuring but not absolute**: reduce perceived risk with concrete controls, human validation and data-handling explanations rather than vague superlatives.
- **Local and specific**: use Moroccan accounting context where evidenced, including MAD, ICE, TVA, fiduciary/accounting-firm vocabulary and compatible export formats.
- **Professional, accessible French**: concise sentences, direct benefits, limited jargon, no startup-hype tone.
- **Human-in-control**: present AI as an assistant that extracts and prepares; do not imply that professional accounting judgment has been removed.

## Preferred message structure

1. Name the operational friction in the user's language.
2. Show the simple intake path: WhatsApp, upload, PDF, scan or photo when relevant.
3. Explain what Klerbot does next: extraction, consistency checks, organization and export preparation.
4. Make the human validation/control point explicit where the workflow depends on it.
5. Add a trust or operational proof point only when supported by current product evidence.
6. End with one clear action: start a trial, see the workflow, request a demo, upload a document, or review an export.

## Claim discipline

Allowed only when supported by current evidence:
- Klerbot can centralize accounting documents received through supported intake channels.
- It can extract invoice/accounting fields and run consistency checks such as ICE/TVA validation.
- It can prepare structured accounting exports for supported formats/configurations.
- The product includes a manual validation/control stage.

Require fresh verification before publishing:
- security absolutes such as "end-to-end encryption";
- "no data shared with third parties" or equivalent privacy absolutes;
- guaranteed compliance, guaranteed accuracy or guaranteed processing time;
- exact trial length, pricing, integrations or export formats if these are not read from current product configuration/content;
- customer numbers, testimonials, savings percentages or ROI claims.

## Avoid

- "Klerbot replaces your accountant/comptable."
- "100% accurate", "zero errors", "fully compliant" or similar guarantees.
- Generic AI hype that hides the concrete workflow.
- Invented customer stories, metrics or security certifications.
- Hard-coded pricing/trial details when the product exposes them dynamically.

## Composition

Use this Skill as context with the reusable writer responsible for the format, for example:

- `linkedin-post-writing` + `klerbot-brand-voice`
- `linkedin-article-writing` + `klerbot-brand-voice`
- `instagram-caption-writing` + `klerbot-brand-voice`
- `social-content-repurposing` + `klerbot-brand-voice`

## Output

A Klerbot voice brief or copy review containing audience, message angle, allowed claims, claims requiring verification, tone corrections and the reusable writing Skill to apply for the final format.