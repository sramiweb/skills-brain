---
name: klerbot-sales-messaging
description: Use when Klerbot sales or outbound work needs approved value themes, buyer-specific argumentation, objection framing, or claim boundaries. Do not use as a generic email-writing method and do not authorize sending messages.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "0.1.0"
  category: klerbot
---

# Klerbot Sales Messaging

## Purpose

Provide Klerbot-specific commercial message ingredients so generic sales and writing Skills can personalize outreach without inventing benefits, guarantees, integrations or customer proof.

This Skill supplies **what may be argued and how it maps to Klerbot buyer pains**. It does not perform lead qualification, write every channel format, select recipients, or authorize delivery.

## Buyer and user framing

### Decision/buyer context

Current product evidence identifies the paying organization as a Moroccan accounting firm / fiduciary. A real mission must still identify the actual decision maker rather than assuming a title.

### Operational users

Accounting-team collaborators are likely to care about workload, document organization, anomaly review, validation and export flow.

### End-user/client context

Artisans/TPE/PME contacts benefit from low-friction document submission, notably through WhatsApp or direct upload. They are product users, not automatically the commercial buyer.

## Approved value themes

Use only when relevant to observed prospect pain:

1. **Centralize scattered accounting documents**
   - Connect to the pain of photos, PDFs, scans or other document sources being dispersed.
   - Do not claim support for a channel that is not currently evidenced.

2. **Reduce repetitive preparation and re-entry**
   - Explain that Klerbot extracts structured accounting fields for review.
   - Do not promise a fixed percentage of time saved without measured evidence.

3. **Surface inconsistencies before validation/export**
   - ICE, TVA, arithmetic or duplicate-related checks may be discussed when current product evidence supports them.
   - Frame them as controls/signals, never guaranteed tax compliance.

4. **Keep the accounting team in control**
   - AI prepares/proposes; the professional validates, corrects and exports.
   - Useful for accuracy/control objections and to avoid "AI replaces accountant" framing.

5. **Fit the downstream accounting workflow**
   - Discuss supported exports or integrations only after verifying the current format/configuration.
   - Never invent native integration when the product only provides an export.

6. **Manage multiple client dossiers in one workflow**
   - Relevant for firms handling repeated document flows across clients.
   - Do not invent a maximum or minimum dossier count.

## Message construction

For a commercial message:

1. Start from one **observed or strongly evidenced prospect pain**, not a generic feature list.
2. Connect that pain to one or two approved Klerbot value themes.
3. Add one current, verifiable product proof point.
4. Address the most likely blocker using factual product behavior, not reassurance alone.
5. Use `klerbot-brand-voice` for tone and claim discipline.
6. Use a generic channel Skill such as `email-personalization` for the final email format.
7. End with a single low-friction CTA supported by the current commercial flow.

## Objection framing

### "L'IA peut se tromper"

Answer with the actual control model: extraction/preparation plus anomaly surfacing and human validation. Never answer with an accuracy guarantee.

### "Mes clients ne veulent pas d'une nouvelle application"

When relevant and current, explain the WhatsApp/direct-upload intake options. Do not claim zero behavior change for every client.

### "Est-ce compatible avec mon logiciel comptable ?"

Verify the exact required format first. Distinguish export compatibility from direct integration.

### "Et la sécurité / confidentialité ?"

Use only current verified security/data-handling evidence. Do not repeat absolute privacy, encryption, hosting or compliance claims merely because they appear in marketing copy.

### "Combien ça coûte / combien de temps pour démarrer ?"

Read fresh pricing/trial/onboarding evidence. Do not hard-code price, trial duration or implementation time into evergreen messaging.

## Negative positioning

Avoid:

- attacking accountants or presenting them as obsolete;
- fear-based tax/compliance claims;
- "100% automatique", "zéro erreur", "conforme garanti";
- fabricated ROI, customer logos, testimonials or success metrics;
- pretending an export is a native API integration;
- feature dumping without a prospect-specific pain.

## Composition

Typical composition:

```text
lead-qualification
+ klerbot-ideal-customer-profile
+ klerbot-sales-messaging
+ klerbot-brand-voice
+ email-personalization
```

Each layer has a separate responsibility: qualification, context, approved argumentation, voice, then channel-specific writing.

## Guardrails

- This Skill never authorizes outreach or sending.
- Personalization must use real prospect evidence; do not invent observations about a company.
- Fresh product/commercial evidence overrides stale messaging details.
- Any claim that could materially affect trust, legal/compliance perception or purchasing must be traceable to current evidence.

## Output

A Klerbot sales-message brief containing buyer/user role, observed pain, selected value themes, proof points, objections, claims requiring verification, prohibited claims and the generic writer/delivery workflow to use next.