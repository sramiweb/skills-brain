# Skills Brain Evaluation Standard

## Status

Normative for Skills Brain schema v2.1 and the Q0-Q5 governance model.

## Goal

A Skill is not trusted because its documentation looks good. Trust must be earned through progressively stronger evidence. Evaluation and lifecycle promotion are separate operations: an evaluator can recommend promotion, but it cannot activate or deploy a Skill.

## Quality gates

| Gate | Purpose | Evidence |
|---|---|---|
| Q0 | Schema and package contract | `SKILL.md` + `skill.yaml` validate |
| Q1 | Static quality and security consistency | manifest/security/risk checks |
| Q2 | Scenario coverage | `tests/scenarios.yaml` |
| Q3 | Security and policy cases | `tests/security.yaml` when required |
| Q4 | Golden Task execution | verified `evals/golden-results.json` |
| Q5 | Regression evidence | verified `evals/regression-results.json` |

Weights in evaluator v1 are currently Q0 20%, Q1 15%, Q2 15%, Q3 15%, Q4 20%, Q5 15%. Mandatory gates depend on status, risk and `evaluation.golden_tasks`.

## Q4/Q5 evidence lifecycle

Q4 and Q5 use a four-stage process.

```text
Skill package + evaluation definition
        ↓
1. PREPARE
        ↓
content-addressed run request
        ↓
2. EXECUTE
        ↓
external runner observations
        ↓
3. VERIFY
        ↓
independent criterion verification
        ↓
4. FINALIZE
        ↓
canonical *-results.json
        ↓
tooling/evaluator.py
```

The Skills Brain repository does not require a specific runner. AgenticOS, another agent runtime, a deterministic harness or a controlled human workflow may execute the run request.

For the reference AgenticOS path, use `tooling/qualification.py` and `adapters/agenticos/evaluation.py`. Normative runtime separation is documented in `standards/runtime-qualification.md`.

## Prepare

`tooling/eval_harness.py prepare` binds a run to:

- Skill ID and version;
- deterministic `package_sha256`;
- Q4 or Q5 definition hash;
- source commit when available;
- exact task/check IDs;
- a unique `run_id`.

Low-level example:

```bash
python tooling/eval_harness.py prepare \
  skills/agenticos/agenticos-agent-audit \
  --gate Q4
```

For AgenticOS runtime qualification, prefer:

```bash
python tooling/qualification.py prepare \
  skills/engineering/codebase-analysis \
  --gate Q4 \
  --tenant klerbot \
  --agent klerbot-coder \
  --data-class S2 \
  --model glm-5.3:cloud
```

This creates both the canonical `request.json` and a non-authorizing `agenticos-plan.json` bound to the same exact Skill package.

Run requests are generated under `reports/eval-runs/` by default so preparing an evaluation does not mutate the immutable Skill package hash.

## Execute

The runner produces an artifact matching `schemas/eval-runner-results.schema.json`.

Runner observations contain only:

- task ID;
- execution status;
- sanitized output summary;
- artifact references;
- evidence references;
- runtime/model metadata when useful.

The AgenticOS reference runner first produces `schemas/agenticos-eval-observation.schema.json`; `adapters/agenticos/evaluation.py` converts it to canonical runner-results **without semantic scoring**.

A successful worker exit only proves execution completed. It does not prove the Golden Task passed.

Do not copy tenant secrets, credentials, private prompts or raw customer data into the canonical Skills Brain repository merely to satisfy evaluation evidence.

## AgenticOS runtime identity check

For an AgenticOS qualification, the observation must prove the exact upstream:

```text
Skill ID
+ version
+ package_sha256
+ source commit when bound
```

The adapter fails closed when these values differ from the evaluation request. Runtime reputation, model quality or successful exit code cannot compensate for a package mismatch.

## Independent verification

The verifier produces an artifact matching `schemas/eval-verification.schema.json`.

Accepted verification types are:

- `deterministic`;
- `human`;
- `independent_model`.

The verifier must be independent from the runner. `verified_by` must not equal `generated_by`, and `independent` must be true.

For each Q4 item the verifier must check:

- whether the declared expected result is satisfied;
- every criterion from `golden.yaml`;
- every forbidden behavior from `golden.yaml`.

For Q5 the normalized check must verify the declared baseline, metric, direction and `allowed_delta` policy.

Missing checks are not treated as success.

## Verified Q5 baseline

A regression definition that says only `baseline: skill@version` is not enough to calculate a real delta. Q5 runtime qualification therefore requires a separately measured and independently verified baseline artifact conforming to:

```text
schemas/regression-baseline.schema.json
```

Default location:

```text
<skill>/evals/regression-baseline.json
```

The artifact records exact metric values and evidence references. `tooling/qualification.py prepare --gate Q5` refuses to proceed when:

- the baseline artifact is missing;
- `verified` or `verification.independent` is not true;
- its `baseline_id` does not match `regression.yaml`;
- a requested regression metric has no verified baseline value.

The baseline SHA256 is bound into the evaluation request. Finalization refuses a baseline that changes after preparation.

For a first historically qualified Skill with no trustworthy older metrics, the correct action is to measure the historical version now under a controlled benchmark or defer Q5. **Synthetic historical metric values are forbidden.**

## Finalize

`tooling/eval_harness.py finalize` validates request, runner and verification artifacts, then recomputes package and definition hashes. The governed `tooling/qualification.py finalize` additionally checks a bound Q5 baseline before delegating to the harness.

Example:

```bash
python tooling/qualification.py finalize \
  skills/engineering/codebase-analysis \
  --request /secure/eval/request.json \
  --runner-results /secure/eval/runner-results.json \
  --verification /secure/eval/verification.json
```

Finalization fails closed if:

- the Skill changed since `prepare`;
- the evaluation definition changed;
- a bound Q5 baseline changed;
- run IDs differ;
- runner/verifier IDs do not exactly cover the request;
- criterion or forbidden-rule coverage is incomplete;
- runner and verifier identities are the same;
- verification is not independent.

The harness computes scores itself from verification checks. A fully passing item scores 1.0.

## Canonical result

The generated Q4/Q5 result uses `schemas/eval-results.schema.json` v2.0 and records:

- `run_id`;
- gate;
- Skill ID/version;
- `package_sha256`;
- evaluation-definition SHA256;
- source commit when available;
- verification method and identity;
- per-item status, verified flag, score and evidence references.

Generated `*-results.json` files are excluded from `package_sha256`; evaluation evidence must not change the identity of the package it evaluates.

## Evaluator re-validation

`tooling/evaluator.py` does not trust the result file blindly. It independently checks that the result still matches:

- current Skill ID/version;
- current package hash;
- current Q4/Q5 definition hash;
- exact current task/check IDs;
- all result items are `pass`, `verified=true`, score 1.0.

Any Skill or evaluation-definition modification invalidates stale Q4/Q5 evidence and requires a new run.

## Promotion rules

A `candidate` may have incomplete Q4/Q5 evidence while being developed. An `approved` or `active` Skill must satisfy all gates required by its risk/status policy.

No quality score can override a mandatory failed gate.

## Non-goals

This standard does not:

- authorize runtime execution;
- choose a model;
- grant concrete tools;
- deploy a Skill;
- accept self-verification;
- infer success from missing evidence;
- invent Q5 baseline metrics;
- allow runtime feedback to modify a production Skill directly.
