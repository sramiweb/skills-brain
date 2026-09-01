# Learning and Continuous Improvement Standard

## Purpose

Skills Brain accepts validated, privacy-preserving learning signals from runtimes such as AgenticOS and turns reusable knowledge into governed Skill improvements.

Runtime learning and canonical knowledge are intentionally separated:

```text
AgenticOS empirical learning
  -> validated reusable pattern
  -> improvement proposal
  -> evaluation
  -> deliberation/review
  -> approval
  -> Skill vNext
```

Skills Brain never grants itself runtime permissions and never modifies a production runtime directly.

## Memory is not learning

- **Memory** records what happened.
- **Learning** states a pattern or hypothesis supported by evidence.
- **Operationalized knowledge** is a validated learning incorporated through a governed version change.

## Learning maturity

```text
L0 SIGNAL
  -> L1 PATTERN
  -> L2 HYPOTHESIS
  -> L3 VERIFIED_LEARNING
  -> L4 OPERATIONALIZED_KNOWLEDGE
```

A single observation MUST NOT be promoted directly to operationalized knowledge.

## Learning event

A learning event should identify:

- tenant/runtime scope without exposing secrets;
- source type;
- subject;
- expected outcome;
- observed outcome;
- delta;
- evidence references;
- confidence derived from evidence quality;
- candidate learning.

## Retrospective questions

For significant outcomes, the runtime should answer:

1. What happened?
2. What was expected?
3. What worked?
4. What failed?
5. Which assumption was wrong?
6. What should be repeated?
7. What should change?
8. What evidence supports the conclusion?

## Improvement proposals

A proposal MUST state:

- target Skill or protocol;
- current version;
- learning source;
- proposed change;
- evidence;
- expected effect;
- risk;
- tests required;
- rollback or compatibility implications.

## No uncontrolled self-modification

The following MUST NOT be changed automatically from runtime feedback:

- canonical `SKILL.md`;
- `skill.yaml`;
- production policies;
- runtime permissions;
- production code;
- pricing or other business-critical rules.

Runtime systems MAY update statistical reputation signals such as verified success rate, cost, latency, human override rate and tool failure rate.

## Privacy and data minimization

Feedback sent to Skills Brain should be aggregated or pseudonymized. It MUST NOT include credentials, raw customer documents, secrets, private prompts or unnecessary personal data.

## Promotion rule

Tenant-specific learning remains local unless it is:

1. repeated;
2. verified;
3. sufficiently generic;
4. safe to generalize;
5. evaluated against regression and security criteria.

Only then may it become a Skills Brain improvement proposal.
