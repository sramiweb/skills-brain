# Klerbot Skill Pack

Klerbot is the first Golden Tenant used to validate the Skills Brain <-> AgenticOS integration end to end.

This directory contains **portable Klerbot context knowledge**, not AgenticOS runtime agents or permissions.

## Implemented context Skills

The reconciled v2.1 pack contains seven context packages with distinct responsibilities:

### Product and engineering context

- `klerbot-product-context` — verified product, users, business model and workflow context.
- `klerbot-architecture` — technical stack, service boundaries and architecture invariants.
- `klerbot-code-conventions` — repository-specific engineering and validation rules.

### Market and commercial context

- `klerbot-ideal-customer-profile` — evidence-qualified buyer/user roles, fit hypotheses and disqualifiers.
- `klerbot-market-context` — durable positioning and comparison axes; dynamic market claims require fresh research.
- `klerbot-sales-messaging` — approved value themes, objection framing and commercial claim boundaries.
- `klerbot-brand-voice` — audience, tone, message framing and publishing claim discipline.

All seven packages remain `candidate` until their golden-task evaluations provide promotion evidence.

## Source-of-truth rule

Canonical context may be derived from the Klerbot product repository, but Skills Brain must not pretend a snapshot is always current.

When fresher product-repository, customer, pipeline, market or runtime evidence contradicts a Klerbot context Skill:

1. prefer the fresher evidence;
2. label its evidence class and observation date when relevant;
3. report the drift;
4. submit a governed update to the context Skill if the change is stable and reusable.

Product positioning is not automatically customer or market proof. In particular, ICP and market Skills must distinguish verified product roles from positioning hypotheses and independently observed evidence.

## Not allowed here

Do not store:

- AgenticOS tenant bindings;
- MCP connector names that are local implementation details;
- credentials or secrets;
- production server addresses;
- local filesystem paths;
- model API keys;
- runtime approval state;
- tenant-specific execution policies.

Those belong to AgenticOS.

## Generic methods stay generic

Do not create Klerbot-specific duplicates of reusable methodologies.

For example:

```text
linkedin-post-writing
+
klerbot-brand-voice
```

is preferred to:

```text
klerbot-linkedin-post-writing
```

Likewise:

```text
roadmap-prioritization
+
klerbot-product-context
```

is preferred to a `klerbot-roadmap-method` package unless Klerbot later develops a genuinely distinct, independently useful prioritization methodology.

The same rule applies to market research, lead qualification, email personalization, customer health, SaaS metrics, code review, release readiness, SRE diagnosis and security review: reusable methods stay in their generic domain categories and consume Klerbot context only when needed.

## Composition examples

### Engineering review

```text
code-review
+ klerbot-code-conventions
+ klerbot-architecture
```

### Product discovery

```text
product-discovery
+ klerbot-product-context
+ klerbot-ideal-customer-profile
```

### Roadmap

```text
roadmap-prioritization
+ klerbot-product-context
+ klerbot-ideal-customer-profile
```

### Competitor analysis

```text
competitor-analysis
+ klerbot-market-context
+ klerbot-product-context
+ klerbot-ideal-customer-profile
```

### Qualified outbound email

```text
lead-qualification
+ klerbot-ideal-customer-profile
+ klerbot-sales-messaging
+ klerbot-brand-voice
+ email-personalization
```

### Social content

```text
linkedin-post-writing
+ klerbot-brand-voice
+ klerbot-product-context
```

The context Skills add knowledge and constraints. They never widen runtime tool permissions or authorize delivery/actions.

## Target domains

The Golden Tenant should progressively exercise reusable Skills across:

- market intelligence;
- product management;
- customer intelligence;
- revenue analytics;
- growth;
- content;
- sales;
- engineering;
- SRE;
- security/compliance.

## Learning promotion

Klerbot runtime learning remains local to AgenticOS until a pattern is repeated, verified, generic and safe to reuse. Only then should AgenticOS submit a governed Skills Brain improvement proposal.
