# AgenticOS Adapter

This adapter exports canonical Skills Brain metadata for consumption by AgenticOS and defines the portable contracts used to qualify Skills against an AgenticOS/Hermes runtime.

## Responsibility boundary

Skills Brain exports:

- canonical Skill identity and version;
- capabilities and logical tool requirements;
- typed input/output contracts used for governed Skill-to-Skill handoff planning;
- risk, side effects and security declarations;
- evaluation requirements;
- source repository/commit/path;
- deterministic integrity hashes;
- non-authorizing runtime evaluation plans.

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

## Governance export contract v1.1

The v1.1 governance export carries canonical contracts under:

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

### Export

```bash
python adapters/agenticos/export.py \
  skills/services/zabbix-proxi-monitor \
  --repository sramiweb/skills-brain \
  --commit <40-char-commit>
```

The result conforms to `schemas/agenticos-export.schema.json`.

AgenticOS should combine the export with its own `bindings.yaml`, tool-capability mapping and tenant policy. Effective runtime permissions must be an intersection of upstream requirements and local policy; the export must never widen local permissions.

For multi-Skill execution, AgenticOS may consume the typed contract metadata produced by Skills Brain, but it remains responsible for deciding whether the producer output can actually be delivered to the consumer in that tenant and data context.

## Runtime qualification adapter

`adapters/agenticos/evaluation.py` is the Skills Brain side of the Q4/Q5 runtime qualification bridge.

It has two responsibilities only:

```text
Skills Brain request.json
        ↓
plan
        ↓
agenticos-plan.json

AgenticOS observation.json
        ↓
collect
        ↓
runner-results.json
```

It does **not**:

- invoke AgenticOS;
- invoke Hermes or an LLM;
- grant execution permission;
- choose runtime tools;
- score model output;
- declare a Golden Task PASS;
- replace the independent verifier.

### Build an AgenticOS plan

Normally use the higher-level governed CLI:

```bash
python tooling/qualification.py prepare \
  skills/engineering/codebase-analysis \
  --gate Q4 \
  --tenant klerbot \
  --agent klerbot-coder \
  --data-class S2 \
  --model glm-5.3:cloud
```

The generated plan conforms to:

```text
schemas/agenticos-eval-plan.schema.json
```

Every plan contains:

```json
{"authorization": "not_granted"}
```

The runtime must still authorize the execution through its local policy.

### Exact upstream identity

Every job carries the expected:

```text
Skill ID
version
package_sha256
source commit when available
```

The AgenticOS runner must use the normally installed immutable package and return the same identity in its observation. `evaluation.py collect` fails closed on any mismatch.

### Read-only evaluation package context

For code-oriented Golden Tasks, a plan may request a bounded snapshot of the **installed immutable Skill package** as evaluation context. The reference plan includes only:

```text
SKILL.md
skill.yaml
fixtures/**
```

The snapshot is read-only evaluation evidence. It is not a filesystem permission grant and must not expose unrelated tenant files.

### Collect runtime observation

After AgenticOS produces an observation conforming to:

```text
schemas/agenticos-eval-observation.schema.json
```

convert it with:

```bash
python tooling/qualification.py collect \
  --request /secure/eval/request.json \
  --observation /secure/eval/observation.json
```

The resulting `runner-results.json` conforms to `schemas/eval-runner-results.schema.json`.

A successful AgenticOS execution is represented only as `status: completed`. The adapter deliberately does not add `verified: true` or a semantic score. An independent verifier must still evaluate every expected result, criterion and forbidden behavior.

## Q5 baseline rule

A Q5 plan is not valid merely because `regression.yaml` names an older version. It requires independently verified metric values in `regression-baseline.json` conforming to `schemas/regression-baseline.schema.json`.

`tooling/qualification.py prepare --gate Q5` fails closed when that evidence is absent or incomplete. Historical values must be measured; they must not be invented.

See:

- `standards/runtime-qualification.md`
- `standards/evaluation.md`
- `schemas/agenticos-eval-plan.schema.json`
- `schemas/agenticos-eval-observation.schema.json`
- `schemas/regression-baseline.schema.json`

## Runtime verification

Before enabling or qualifying a Skill, AgenticOS should independently recompute `package_sha256` using `standards/integrity.md` and compare it with the pinned export/lock entry. A mismatch must fail closed.
