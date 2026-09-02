# Skills Brain Capability Ontology

`standards/capabilities.yaml` is the canonical machine-readable ontology for skill capabilities and tool capabilities.

## Rules

1. A canonical `skill.yaml` MUST declare only capabilities present in the ontology.
2. `capabilities` describe **what the skill knows how to accomplish**.
3. `requirements.tool_capabilities` describe **what kind of tool access is required**, not a concrete MCP tool name.
4. AgenticOS maps logical tool capabilities to tenant-specific MCP connectors and tools.
5. A Skill MUST NOT name private hosts, tenants, credentials, local mount paths or provider-specific secrets.
6. `reserved` capabilities may be used by new candidate Skills but are not considered production-proven.
7. `deprecated` capabilities must not be introduced by new Skills.

## Example

```yaml
capabilities:
  - database.postgres.diagnose
requirements:
  tool_capabilities:
    - logs.read
    - monitoring.read
```

AgenticOS may map these requirements to different concrete tools per tenant. Skills Brain remains runtime-neutral.

## Resolution order

```text
Mission
  -> required capabilities
  -> candidate Skills
  -> governance eligibility
  -> runtime/tool compatibility
  -> ranking
```

Security eligibility is a filter, not a ranking bonus or penalty.
