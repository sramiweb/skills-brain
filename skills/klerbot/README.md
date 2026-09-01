# Klerbot Skill Pack

Klerbot is the first Golden Tenant used to validate the Skills Brain <-> AgenticOS integration end to end.

This directory contains **portable Klerbot context knowledge**, not AgenticOS runtime agents or permissions.

## Allowed here

Klerbot-specific knowledge packages such as:

- `klerbot-product-context`
- `klerbot-market-context`
- `klerbot-brand-voice`
- `klerbot-ideal-customer-profile`
- `klerbot-sales-messaging`
- `klerbot-code-conventions`
- `klerbot-architecture`
- `klerbot-roadmap-method`

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

Likewise, market research, roadmap prioritization, customer health, SaaS metrics, code review, release readiness and SRE diagnosis should live in their generic domain categories and consume Klerbot context only when needed.

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
