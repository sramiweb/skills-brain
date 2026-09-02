# Deliberation Standard

## Purpose

Skills Brain defines reusable deliberation protocols. AgenticOS decides when a protocol is allowed or required and remains the execution and policy authority.

## Core principles

1. Evidence before opinion.
2. Independent first-round positions to reduce anchoring and groupthink.
3. Mandatory criticism for significant decisions.
4. Preserve dissent; do not collapse disagreement into majority voting.
5. Security or policy vetoes override consensus.
6. The proposer must not be the final judge for high-impact decisions.
7. Human approval remains mandatory when the runtime policy requires it.
8. Deliberation is bounded by rounds, tokens, cost and time.

## Standard phases

```text
EVIDENCE_READY
  -> INDEPENDENT_ANALYSIS
  -> CROSS_EXAMINATION
  -> REVISED_POSITIONS
  -> RISK_REVIEW
  -> JUDGEMENT
  -> RECOMMENDATION
```

A protocol MAY omit CROSS_EXAMINATION for low-cost reviews, but MUST declare that explicitly.

## Canonical roles

- **Advocate**: presents the strongest evidence-based case for the proposal.
- **Critic**: searches for failure modes, hidden assumptions and better alternatives.
- **Domain Expert**: evaluates domain-specific feasibility and consequences.
- **Risk/Security Reviewer**: assesses security, data, compliance and blast radius.
- **Judge/Arbiter**: synthesizes the evidence and arguments without rewriting dissent away.

## Argument contract

Every material argument should contain:

```yaml
claim: "..."
evidence_refs: []
assumptions: []
confidence: 0.0
falsifier: "What observation would prove this claim wrong?"
severity: low
```

## Verdicts

```text
support
support_with_conditions
reject
insufficient_evidence
escalate
```

## Required output

A debate result MUST preserve:

- recommendation;
- confidence based on evidence, not model self-confidence;
- arguments for and against;
- unresolved questions;
- conditions;
- risks;
- dissent;
- missing evidence;
- human-decision requirement.

## Protocol families

The initial canonical protocols are:

- `strategic-debate-v1`: roadmap, pricing, product and major growth decisions;
- `technical-debate-v1`: architecture, code, migration, security and releases;
- `operational-debate-v1`: incidents, remediation, rollback and production operations.

## Pre-mortem

High-impact protocols SHOULD run a pre-mortem before judgement:

> Assume the decision failed after deployment. What are the most plausible reasons?

## Anti-patterns

Do not:

- use simple majority vote as the sole decision rule;
- expose previous participant answers in the first independent round;
- let the proposer silently become the judge;
- continue debating until everyone agrees;
- permit a Council to bypass runtime policy or a security veto;
- treat model confidence as evidence quality.
