# Skills Brain — Verified Reputation v1.0

## Purpose

Reputation is statistical evidence about how a specific Skill version performed in verified runtime outcomes. It refines ranking after eligibility; it is never an authorization signal.

```text
verified runtime Outcomes
  -> privacy/scope filter
  -> exact Skill version grouping
  -> minimum sample gate
  -> conservative statistics
  -> freshness adjustment
  -> reputation report
  -> post-eligibility ranking signal
```

## Authority boundary

Reputation MUST NOT:

- make an ineligible Skill eligible;
- override missing tools, denied data classes, lifecycle state, risk ceiling or runtime incompatibility;
- grant concrete tools, tenants, credentials or execution permissions;
- promote a Skill lifecycle state;
- replace Q0-Q5 evaluation evidence;
- merge tenant-specific empirical evidence into canonical global ranking by default.

## Accepted evidence

The reference aggregator consumes documents conforming to `schemas/outcome.schema.json`.

Only records meeting all of these conditions contribute:

1. `subject.type == skill`;
2. `verified == true`;
3. `verification_score` exists and meets the configured minimum;
4. scope matches the requested report scope.

Unverified outcomes and low-verification observations are ignored rather than converted into weak positive or negative reputation.

## Exact version rule

Reputation is tied to a specific Skill version.

```text
skill-id@1.0.0 reputation != skill-id@1.1.0 reputation
```

The canonical resolver uses reputation only when the report version exactly equals the current manifest version. Historical samples may remain visible, but they cannot score the new version.

This prevents a new Skill revision from inheriting trust it has not yet earned.

## Scope and privacy

Two report scopes exist.

### Global

A global report includes **only generic outcomes without `tenant_hash`**.

Tenant-scoped observations are excluded even if they are numerous or high quality.

The canonical Skills Brain resolver accepts only global reputation reports.

### Tenant

A tenant report includes only outcomes whose pseudonymous `tenant_hash` exactly matches the requested tenant.

Tenant reports are intended for local runtimes such as AgenticOS and MUST NOT influence the canonical Skills Brain resolver.

This preserves:

```text
AgenticOS tenant empirical reputation = local
Skills Brain reusable/global reputation = generic verified evidence only
```

## Minimum sample gate

A subject remains visible below `minimum_samples`, but:

```json
{
  "eligible_for_ranking": false,
  "reputation_score": null
}
```

The default reference threshold is 5 verified observations. Consumers may choose a stricter threshold.

## Conservative success estimate

The reference implementation uses the 95% Wilson lower bound rather than raw success rate as its main reliability component.

This prevents a Skill with one successful run from receiving the same confidence as a Skill with many successful verified runs.

The report preserves both:

- `verified_success_rate`;
- `wilson_lower_bound`.

## Reputation score v1

For a subject above the minimum sample threshold:

```text
base =
  0.60 * Wilson success lower bound
+ 0.20 * average verification score
+ 0.10 * (1 - human override rate)
+ 0.10 * (1 - tool failure rate)

reputation = base * freshness_factor
```

The score is bounded to `[0,1]`.

`human_override_rate` is treated as a reliability warning, not a moral or quality judgment. A future typed override taxonomy may distinguish rejection, correction and benign intervention.

## Freshness

When `occurred_at` is available, the reference implementation applies:

```text
<= 90 days   -> 1.00
<= 180 days  -> 0.90
<= 365 days  -> 0.75
> 365 days   -> 0.50
```

If no timestamp is available, the conservative compatibility factor is `0.75`.

For reproducibility, `tooling/reputation.py` accepts `--as-of`.

## Cost and latency

The report also includes average cost and duration when present. They are descriptive in v1 and do not directly affect reputation score.

This avoids silently optimizing for cheap or fast behavior at the expense of correctness. Future routing policy may explicitly trade quality, cost and latency.

## Resolver use

When a valid global report is provided with `reputation_report`, resolver v1.1 keeps its existing eligibility process unchanged.

For an eligible exact-version Skill with rankable reputation:

```text
final ranking score = 0.90 * existing resolver score
                    + 0.10 * reputation score
```

Without rankable reputation, the existing resolver score is preserved exactly.

A reputation score can reorder already eligible candidates; it can never erase a rejection reason.

## Outcome timestamp

`schemas/outcome.schema.json` now accepts optional `occurred_at` for recency calculations. It is optional for backward compatibility, but runtimes SHOULD provide it for new evidence.

## Reference implementation

- `tooling/reputation.py`
- `schemas/outcome.schema.json`
- `schemas/reputation-report.schema.json`
- `tooling/resolver.py`
- `tests/test_reputation.py`
