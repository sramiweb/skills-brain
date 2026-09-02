# Skills Brain Capability Resolution

Capability resolution selects candidate Skills. It does **not** authorize execution.

## Input

A resolution request conforms to `schemas/resolution-request.schema.json` and may include:

- requested capabilities;
- available logical tool capabilities;
- allowed lifecycle statuses;
- maximum risk;
- data class;
- runtime/version compatibility context;
- result limit and rejected-candidate explanation.

Tenant identity, credentials and concrete MCP tools are intentionally absent. Those belong to AgenticOS or another consuming runtime.

## Order of operations

Eligibility is evaluated before ranking:

```text
request validation
  -> ontology validation
  -> capability overlap
  -> lifecycle eligibility
  -> risk ceiling
  -> required tool availability
  -> data-class eligibility
  -> runtime compatibility
  -> ranking
```

A ranking score must never compensate for an eligibility failure.

## Fail-closed rules

- Unknown requested capabilities are rejected.
- Unknown available tool capabilities are rejected.
- Quarantined Skills are never eligible.
- Missing required tool capabilities reject the candidate.
- A requested data class is rejected when the Skill does not allow it.
- If a Skill has no data-class declaration, a data-class-aware request rejects it by default unless the caller explicitly allows unspecified data classes.
- When explicit runtime compatibility is required, an unspecified runtime declaration rejects the candidate.
- Unsupported compatibility syntax fails closed.

## Partial capability coverage

A Skill may cover only part of a multi-capability request. Such a candidate may be returned for future composition, but a full match is always ranked ahead of partial matches.

The response explicitly reports:

- `full_match`;
- `capability_coverage`;
- matched capabilities;
- missing capabilities.

## Ranking

The v1 resolver ranks eligible candidates using:

```text
55% capability coverage
25% measured evaluation score
10% lifecycle maturity
10% risk fitness
```

The evaluation component uses a measured Q0-Q5 score when available. Missing evaluation evidence contributes `0`; the manifest's `minimum_score` threshold is never treated as achieved quality.

The formula is a ranking heuristic, not an authorization rule and not a permanent compatibility promise.

## Runtime boundary

Every response includes:

```json
{"authorization": "not_granted"}
```

AgenticOS must still apply local tenant, binding, MCP tool, network, approval and policy checks before execution.
