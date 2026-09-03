# Klerbot Skill Pack

Klerbot is the first Golden Tenant used to validate the Skills Brain <-> AgenticOS integration end to end.

This directory contains **portable Klerbot context knowledge**, not AgenticOS runtime agents or permissions.

## Implemented context Skills

Wave 1 establishes four context packages that have distinct responsibilities:

- `klerbot-product-context` — verified product, users, business model and workflow context.
- `klerbot-architecture` — technical stack, service boundaries and architecture invariants.
- `klerbot-code-conventions` — repository-specific engineering and validation rules.
- `klerbot-brand-voice` — audience, tone, message framing and claim discipline.

These packages are `candidate` until their golden-task evaluations are recorded.

## Planned context packages

Additional Klerbot-specific context is valid only when it contains real, maintained knowledge rather than placeholders. Candidate areas include:

- `klerbot-market-context`
- `klerbot-ideal-customer-profile`
- `klerbot-sales-messaging`

Do not create them merely to mirror an AgenticOS agent. Their content must remain independently useful and materially different from an existing generic Skill.

## Source-of-truth rule

Canonical context may be derived from the Klerbot product repository, but Skills Brain must not pretend a snapshot is always current.

When fresher product-repository or runtime evidence contradicts a Klerbot context Skill:

1. prefer the fresher evidence;
2. report the drift;
3. submit a governed update to the context Skill if the change is stable and reusable.

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

The same rule applies to market research, customer health, SaaS metrics, code review, release readiness, SRE diagnosis and security review: reusable methods stay in their generic domain categories and consume Klerbot context only when needed.

## Composition examples

```text
code-review
+ klerbot-code-conventions
+ klerbot-architecture
```

```text
product-discovery
+ klerbot-product-context
```

```text
roadmap-prioritization
+ klerbot-product-context
```

```text
linkedin-post-writing
+ klerbot-brand-voice
+ klerbot-product-context
```

The context Skills add knowledge and constraints. They never widen runtime tool permissions.

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
