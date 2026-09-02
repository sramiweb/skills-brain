# Skills Brain — Runtime Qualification Standard

## Purpose

Runtime qualification turns a canonical Skill from an evaluation definition into **verified execution evidence** without allowing Skills Brain to execute production tools, self-judge a model output or fabricate historical baselines.

The reference flow is:

```text
Skills Brain PREPARE
        ↓
content-addressed request.json
        ↓
Runtime adapter plan
        ↓
AgenticOS / Hermes EXECUTION
        ↓
AgenticOS observation.json
        ↓
Skills Brain COLLECT
        ↓
runner-results.json
        ↓
Independent VERIFICATION
        ↓
verification.json
        ↓
Skills Brain FINALIZE
        ↓
golden-results.json / regression-results.json
        ↓
Evaluator Q4 / Q5
```

## Authority separation

### Skills Brain may

- bind an evaluation run to exact Skill ID/version/package hash;
- bind the run to the exact evaluation-definition hash;
- generate a runtime-specific execution plan;
- verify that runtime observations came from the expected upstream Skill package;
- convert runtime observations into the canonical runner-results contract;
- validate independent verification coverage;
- finalize Q4/Q5 evidence.

### Skills Brain must not

- hold runtime credentials;
- grant AgenticOS permissions;
- execute production actions;
- silently widen the runtime tool set;
- declare semantic PASS based only on a runtime exit code;
- use the same identity as runner and verifier;
- invent baseline values for Q5.

## AgenticOS runner responsibilities

The AgenticOS qualification runner must:

1. consume `schemas/agenticos-eval-plan.schema.json`;
2. verify that the installed runtime index contains the exact Skill ID/version/commit/package hash expected by the plan;
3. use the normal Skills Brain binding so Hermes must load the exact `skill_view()` methodology;
4. make evaluation package context available read-only and only within the requested size/path bounds;
5. preserve the configured tenant, data class, sandbox, model routing and MCP policy;
6. record the effective allowed tools;
7. produce an observation conforming to `schemas/agenticos-eval-observation.schema.json`;
8. never evaluate its own answer against Golden Task criteria.

Runtime execution authority remains AgenticOS-local. The plan always contains:

```json
{"authorization": "not_granted"}
```

## Package context

For code-oriented Golden Tasks, AgenticOS may render a bounded read-only snapshot of the installed Skill package into the mission context. The snapshot must be taken from the **installed immutable package whose `package_sha256` matches the evaluation request**.

The reference AgenticOS plan requests:

```text
SKILL.md
skill.yaml
fixtures/**
```

This is evaluation context, not an additional runtime permission. It must not expose unrelated tenant files or secrets.

## Runner observation is not verification

A successful worker exit means only that execution completed.

The AgenticOS adapter converts:

```text
succeeded -> completed
failed/timeout/cancelled -> error
skipped -> skipped
```

It does **not** add `verified=true`, does not calculate Golden scores and does not decide whether expected behavior matched.

## Independent verification

The verifier receives:

- the exact evaluation request;
- runner-results / runtime evidence;
- expected result;
- every criterion;
- every forbidden behavior.

The verifier must be a different identity from the runner and produce `schemas/eval-verification.schema.json` with `independent: true`.

Allowed verifier types:

- deterministic;
- human;
- independent model.

A second model should preferably use a different model family or context path when practical.

## Q4 Golden Task qualification

Reference command:

```bash
python tooling/qualification.py prepare \
  skills/engineering/codebase-analysis \
  --gate Q4 \
  --tenant klerbot \
  --agent klerbot-coder \
  --data-class S2 \
  --model glm-5.3:cloud \
  --output-dir /secure/eval/codebase-analysis-q4
```

The command creates:

```text
request.json
agenticos-plan.json
```

After AgenticOS produces `observation.json`:

```bash
python tooling/qualification.py collect \
  --request /secure/eval/codebase-analysis-q4/request.json \
  --observation /secure/eval/codebase-analysis-q4/observation.json
```

This produces `runner-results.json`.

After independent verification:

```bash
python tooling/qualification.py finalize \
  skills/engineering/codebase-analysis \
  --request /secure/eval/codebase-analysis-q4/request.json \
  --runner-results /secure/eval/codebase-analysis-q4/runner-results.json \
  --verification /secure/eval/codebase-analysis-q4/verification.json
```

Only then may `golden-results.json` become canonical Q4 evidence.

## Q5 regression baseline

Q5 must never infer historical values from a version string.

A Q5 run requires independently verified baseline evidence conforming to:

```text
schemas/regression-baseline.schema.json
```

Default location:

```text
<skill>/evals/regression-baseline.json
```

The baseline identifies:

- baseline Skill/version;
- optional historical package hash and source commit;
- generator;
- independent verifier;
- exact metric values;
- evidence references for every metric.

`tooling/qualification.py prepare --gate Q5` fails closed when this artifact is absent, unverified, mismatched with `regression.yaml`, or missing a required metric.

The baseline file hash is bound into `request.json`. Finalization refuses a baseline that changed after preparation.

### Bootstrap rule

For the first historically qualified version, there may be no trustworthy earlier baseline. In that case the project must **measure the historical version now** using a controlled benchmark or explicitly defer Q5. It must not create synthetic historical metrics merely to promote the new version.

A bootstrap baseline becomes valid only after its own measurements and independent verification are complete.

## Evidence storage

Runtime artifacts may contain model output and should normally remain in a controlled evaluation workspace. Only the canonical `*-results.json` files intended by the governance process should be considered for repository inclusion.

Never commit:

- secrets;
- tenant customer payloads;
- raw private prompts;
- credentials;
- unredacted sensitive runtime traces.

## Qualification status

```bash
python tooling/qualification.py status skills/engineering/codebase-analysis
```

The command reports package hashes and whether Q4/Q5 definitions, verified results and Q5 baseline evidence currently exist. It does not claim that an absent result passed.

## First Golden Path

The first reference qualification is:

```text
codebase-analysis
  -> AgenticOS klerbot-coder
  -> Hermes
  -> exact skill_view(codebase-analysis)
  -> read-only package fixture context
  -> runtime observation
  -> independent verification
  -> Q4 evidence
```

Q5 follows only after a verified `codebase-analysis@0.1.0` regression baseline exists.
