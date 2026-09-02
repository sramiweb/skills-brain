# AgenticOS Adapter

This adapter exports canonical Skills Brain metadata for consumption by AgenticOS.

## Responsibility boundary

Skills Brain exports:

- canonical Skill identity and version;
- capabilities and logical tool requirements;
- typed input/output contracts used for governed Skill-to-Skill handoff planning;
- risk, side effects and security declarations;
- evaluation requirements;
- source repository/commit/path;
- deterministic integrity hashes.

Skills Brain does **not** export or grant:

- tenants;
- runtime agents;
- MCP connectors;
- concrete MCP tools;
- credentials;
- filesystem mounts;
- network profiles;
- approval decisions;
- data-transfer authorization;
- execution permissions.

Those remain AgenticOS-local policy and bindings.

## Export contract v1.1

The v1.1 export carries canonical contracts under:

```json
{
  "skill": {
    "contracts": {
      "inputs": [],
      "outputs": []
    }
  }
}
```

A contract describes expected schema and data classification. It does not authorize an actual runtime payload transfer. AgenticOS must independently check tenant, data-class, policy and execution context before moving data between workers or Skills.

## Export

```bash
python adapters/agenticos/export.py \
  skills/services/zabbix-proxi-monitor \
  --repository sramiweb/skills-brain \
  --commit <40-char-commit>
```

The result conforms to `schemas/agenticos-export.schema.json`.

AgenticOS should combine the export with its own `bindings.yaml`, tool-capability mapping and tenant policy. Effective runtime permissions must be an intersection of upstream requirements and local policy; the export must never widen local permissions.

For multi-Skill execution, AgenticOS may consume the typed contract metadata produced by Skills Brain, but it remains responsible for deciding whether the producer output can actually be delivered to the consumer in that tenant and data context.

## Runtime verification

Before enabling a Skill, AgenticOS should independently recompute `package_sha256` using `standards/integrity.md` and compare it with the pinned export/lock entry. A mismatch must fail closed.
