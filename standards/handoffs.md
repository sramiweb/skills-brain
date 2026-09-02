# Skills Brain — Typed Skill Handoffs v1.0

## Purpose

A composition needs more than an execution order. When one Skill consumes another Skill's output, the handoff must state **what is transferred, which schema it follows and which data class it carries**.

Typed handoffs remain planning metadata. They do not grant data access or runtime permissions.

## Manifest contracts

A Skill may declare typed contracts under `contracts`.

### Output contract

```yaml
contracts:
  outputs:
    - id: discovery-result
      schema_id: product.discovery-result.v1
      data_class: S2
```

An output contract declares:

- a stable local `id`;
- a portable `schema_id` describing the semantic payload contract;
- the data classification carried by the output;
- an optional description.

### Input contract

```yaml
contracts:
  inputs:
    - id: discovery-result
      schema_id: product.discovery-result.v1
      source: skill
      required: true
      from_capabilities:
        - product.discover
      allowed_data_classes:
        - S0
        - S1
        - S2
```

An input contract declares:

- the expected `schema_id`;
- whether the value comes from `mission`, `skill` or `either`;
- whether the input is required;
- allowed producer capabilities for Skill-to-Skill handoffs;
- accepted data classes.

`source: skill` requires at least one `from_capabilities` entry.

## Matching rules

For a `source: skill` input, the composer may create a handoff only when all of the following are true:

1. producer and consumer are already in the eligible selected composition;
2. the producer exposes an output with the exact same `schema_id`;
3. the producer implements one of the declared `from_capabilities`;
4. the output `data_class` is explicitly listed in `allowed_data_classes`;
5. producer and consumer are not the same Skill.

No semantic guessing is permitted. Similar names, descriptions or adjacent capabilities do not satisfy a schema mismatch.

## Required inputs

If a required `source: skill` input has no compatible provider, composition fails closed with `status: unresolved`.

Typical blockers include:

```text
handoff_unresolved:<consumer>:<input>:<schema_id>
handoff_data_class_denied:<consumer>:<input>:<observed classes>
```

An optional Skill input may remain unresolved without invalidating the plan.

## Data classification

The producer labels the output data class. The consumer explicitly lists accepted data classes.

A handoff is valid only by exact membership:

```text
producer output data_class ∈ consumer allowed_data_classes
```

The composer does not downgrade, redact or transform a data class automatically. If transformation is required, it must be represented by an explicit eligible Skill or runtime-controlled mechanism.

## Ordering

A valid typed handoff creates a directed planning edge:

```text
producer Skill -> consumer Skill
```

The composer includes these edges in topological ordering together with explicit Skill dependencies.

A cycle created by dependency or handoff edges invalidates the composition.

## Runtime authority

A handoff means only that the plan expects a compatible payload transfer.

It does not authorize:

- the producer to read source data;
- the consumer to receive tenant data;
- a concrete transport or MCP connector;
- persistence;
- credentials;
- cross-tenant sharing.

AgenticOS or another runtime must still enforce local tenant, data-class, tool, network and approval policy.

## Cross-tenant rule

Typed handoffs do not change the default rule that empirical tenant data is tenant-local. A portable schema may be reused across tenants, but actual runtime payload movement remains governed locally.

## Example

The Product flow can declare:

```text
product-discovery
  output: product.discovery-result.v1 / S2
        ↓
feature-specification
  input:  product.discovery-result.v1 / accepts S0,S1,S2
```

The composer can then produce the explicit handoff and order `product-discovery` before `feature-specification` without granting execution authority.

## Reference implementation

- `schemas/skill.schema.json` (`contracts`)
- `tooling/validate.py`
- `tooling/composer.py`
- `schemas/composition-result.schema.json`
- `tests/test_handoff_contracts.py`
- `tests/test_composer.py`
