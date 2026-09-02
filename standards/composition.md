# Skills Brain — Governed Composition v1.1

## Purpose

Composition is used when a requested capability set cannot or should not be satisfied by an arbitrary collection of Skills. The composer builds a **minimum sufficient plan** from Skills that already satisfy eligibility constraints.

Composition is advisory. It never grants runtime authorization.

```text
Mission capabilities
  -> eligibility
  -> minimum sufficient Skill set
  -> dependency closure
  -> conflict / supersession checks
  -> typed handoff resolution
  -> dependency + data-flow order
  -> combined logical requirements
  -> composite risk / side effects
  -> authorization: not_granted
```

## Authority boundary

The composer may state what a plan requires. It may not grant:

- tenant access;
- concrete MCP tools;
- credentials;
- network access;
- filesystem mounts;
- approval;
- data-transfer authorization;
- execution authority.

The union of `tool_capabilities` is a **planning requirement only**. A runtime such as AgenticOS must still calculate effective permissions from its local bindings and policies.

## Eligibility first

Quality, convenience or coverage must never override an eligibility failure.

Every selected Skill and every transitive dependency must satisfy the same relevant constraints used by the resolver:

- lifecycle status;
- risk ceiling;
- available logical tools;
- data class;
- runtime compatibility.

A dependency that fails eligibility makes that composition invalid.

## Minimum sufficient set

The deterministic v1 algorithm prefers, in order:

1. the smallest total number of Skills, including transitive dependencies;
2. the highest average measured eligible quality/ranking signal;
3. the lowest composite risk;
4. a stable lexical tie-break.

If one eligible Skill covers the full requested capability set, it is preferred over an unnecessary multi-Skill bundle.

## Dependencies

Dependencies are declared through:

```yaml
requirements:
  skills: [...]

relationships:
  requires: [...]
```

The composer closes dependencies recursively. Missing dependencies, dependency cycles and ineligible dependencies are blocking conditions.

Dependencies must execute before dependants in the returned topological order.

## Typed handoffs

A selected Skill may declare typed `contracts.inputs` and `contracts.outputs`.

For every required input with `source: skill`, the composer must find a selected eligible producer whose:

- capability matches `from_capabilities`;
- output `schema_id` exactly matches the consumer input `schema_id`;
- output `data_class` is explicitly accepted by the consumer.

A valid handoff creates a producer-to-consumer ordering edge. Missing providers, schema mismatch and data-class mismatch fail closed.

The composer never infers schema compatibility from names or descriptions and never downgrades a data class implicitly.

Detailed rules are in `standards/handoffs.md`.

## Conflicts and supersession

If a selected Skill declares another selected Skill in `relationships.conflicts`, the composition is invalid.

A bundle containing a Skill together with a Skill it declares in `relationships.supersedes` is rejected to avoid silently combining replacement and superseded behavior.

`extends` and `composes` remain descriptive relationships in v1 unless they also create explicit requirements or conflicts.

## Capability ownership

For every requested capability the result contains:

- all selected providers;
- one deterministic owner.

Ownership is a planning responsibility, not authorization. The owner is chosen only among already eligible selected Skills.

## Composite risk and side effects

The composite risk is at least the maximum declared risk of any member.

The composite side-effect class is the strongest declared member class according to:

```text
none < local < reversible < external < destructive < unknown
```

The composer does not invent an extra risk increase without explicit evidence of a new cross-Skill effect. Typed handoffs expose data-flow evidence that future policy layers may use for additional risk or approval rules.

## Failure semantics

The composer fails closed and returns `status: unresolved` when it cannot produce a valid plan.

Examples:

- requested capability has no eligible provider;
- a required Skill is absent;
- a required Skill is ineligible;
- selected Skills conflict;
- a dependency or handoff cycle exists;
- dependency closure exceeds `max_skills`;
- superseded and replacement Skills would coexist;
- a required typed handoff has no exact schema provider;
- producer output data class is not accepted by the consumer.

Missing capabilities and missing payload contracts are never replaced by semantically adjacent alternatives.

## Runtime contract

Every result must contain:

```json
{
  "authorization": "not_granted"
}
```

A consuming runtime may accept the plan, reject it, further restrict it, require debate/approval, or resolve it differently according to local policy. Typed handoff metadata does not itself authorize the runtime payload transfer.

## Reference implementation

- `tooling/composer.py`
- `schemas/composition-request.schema.json`
- `schemas/composition-result.schema.json`
- `schemas/skill.schema.json`
- `standards/handoffs.md`
- `tests/test_composer.py`
- `tests/test_handoff_contracts.py`
