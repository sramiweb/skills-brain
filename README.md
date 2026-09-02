# Skills Brain v2.1

> **Open Skill Intelligence & Governance Plane for AI agents**

Skills Brain defines, evaluates, governs and evolves reusable Agent Skills. It is intentionally independent from any single runtime.

## Positioning

```text
Skills Brain = canonical skills, capabilities, protocols, evaluation and reusable knowledge
AgenticOS    = orchestration, runtime bindings, tenant policy, approvals and execution authority
Hermes       = agentic reasoning and execution runtime
MCP          = tools and actions
LiteLLM      = model routing gateway
```

A Skill describes **how to perform a capability**. It never grants itself runtime permissions.

```text
Skill = HOW to do something
Tool  = WITH WHAT to act
```

## Core principles

- Skills are portable, versioned and canonically identified.
- Canonical Skills use logical capabilities rather than vendor-specific runtime bindings.
- AgenticOS-specific tenants, connectors, credentials and tool permissions do not belong in canonical Skills.
- Evidence is required before trust.
- Security, compatibility and integrity checks are fail-closed.
- Eligibility is checked before ranking or composition.
- Verified reputation may refine ranking only after eligibility and only for the exact Skill version.
- Tenant-specific empirical reputation remains runtime-local by default.
- Composition plans requirements and typed data handoffs; it never grants runtime permissions or data-transfer authority.
- Runtime qualification separates execution from independent verification and never treats a successful worker exit as semantic PASS.
- Runtime outcomes may produce improvement proposals, never uncontrolled production self-modification.
- A small set of evaluated Skills is more valuable than a large unmeasured catalog.

## Repository architecture

```text
skills-brain/
├── standards/          # Lifecycle, capabilities, evaluation, runtime qualification, resolution, reputation, composition, handoffs, integrity, deliberation, learning
├── schemas/            # Machine contracts
├── core/               # Governance meta-skills
├── skills/             # Canonical skill packages
├── protocols/          # Debate and decision protocols
├── catalog/            # Generated indexes
├── adapters/           # Runtime/platform export + evaluation contracts
├── tooling/            # Validation, evaluation, qualification, reputation, catalog, resolver, composer and integrity tooling
├── examples/           # Example requests/contracts
├── tests/              # Repository/tooling tests
└── .github/workflows/  # CI
```

`skills/` is the only canonical Skill package location.

## Skill package

New Skills use `schema_version: "2.1"` and the strict `schemas/skill.schema.json` contract.

Minimum package:

```text
<skill>/
├── SKILL.md
└── skill.yaml
```

Optional source assets include `README.md`, `CHANGELOG.md`, `tests/`, `evals/`, `references/`, `resources/`, `scripts` and `fixtures/`.

A v2.1 Skill may also declare machine-readable `contracts.inputs` and `contracts.outputs` for governed Skill-to-Skill data flow.

The v2.0 schema remains only for compatibility/migration of historical manifests.

## Capability ontology

`standards/capabilities.yaml` defines canonical Skill capabilities and logical tool capabilities.

Examples:

```text
product.discover
sales.lead.qualify
engineering.code.review
sre.application.health
database.postgres.diagnose
```

Logical requirements such as `filesystem.read`, `logs.read` or `monitoring.read` are mapped by the consuming runtime to concrete tools.

## Capability resolver

`tooling/resolver.py` resolves requested capabilities to **eligible candidates**, not authorized executions.

Eligibility runs before ranking:

```text
ontology
-> capability overlap
-> lifecycle status
-> risk ceiling
-> required tools
-> data class
-> runtime compatibility
-> ranking
```

A high quality or reputation score cannot override a missing tool, incompatible data class, excess risk or denied lifecycle state.

The resolver returns:

```json
{"authorization": "not_granted"}
```

Example:

```bash
python tooling/resolver.py examples/resolution-request.json
```

Base ranking uses capability coverage, measured Q0-Q5 quality, lifecycle maturity and risk fitness. Missing evaluation evidence contributes zero. `minimum_score` is a threshold and is never treated as achieved quality.

### Verified reputation

`tooling/reputation.py` aggregates verified runtime Outcomes into version-specific reputation evidence.

```text
verified Outcomes
-> scope filter
-> exact Skill version
-> minimum sample gate
-> Wilson success lower bound
-> verification / overrides / tool failures
-> freshness
-> reputation report
```

Global reports include only generic outcomes without `tenant_hash`. Tenant reports can be generated for runtime-local use but the canonical resolver deliberately rejects them.

Example:

```bash
python tooling/reputation.py /path/to/outcomes \
  --scope global \
  --minimum-samples 5 \
  --as-of 2026-09-02T00:00:00Z \
  --output reports/reputation.json
```

Then a resolution request may reference:

```json
{"reputation_report": "reports/reputation.json"}
```

Reputation is used only when it matches the **exact current Skill version** and has enough verified samples. Without eligible reputation evidence, the prior resolver score is preserved. With reputation, it is a bounded post-eligibility refinement; it never changes authorization or rejection reasons.

See `standards/resolution.md`, `standards/reputation.md`, `schemas/resolution-request.schema.json` and `schemas/reputation-report.schema.json`.

## Governed Skill composer

`tooling/composer.py` builds a deterministic minimum sufficient plan when multiple capabilities are requested.

```text
requested capabilities
-> resolver-grade eligibility
-> minimum sufficient Skill set
-> transitive dependency closure
-> dependency eligibility
-> conflicts / supersession
-> typed handoff resolution
-> dependency + data-flow ordering
-> combined logical requirements
-> composite risk / side effects
-> authorization: not_granted
```

Important properties:

- every selected Skill and transitive dependency must remain eligible;
- one full-match Skill is preferred over an unnecessary bundle;
- missing capabilities are never replaced by semantically adjacent capabilities;
- `requirements.skills` and `relationships.requires` are closed recursively;
- missing, cyclic or ineligible dependencies block composition;
- explicit conflicts and replacement/superseded pairs block composition;
- `max_skills` applies to the complete closure, not just the initial candidates;
- required Skill-to-Skill inputs need an exact compatible typed output;
- typed handoffs add producer → consumer ordering edges;
- data classes must be explicitly accepted by the consumer; no implicit downgrade occurs;
- the union of `tool_capabilities` is planning information only, never granted permissions;
- quality is used only after eligibility and cannot bypass a rejection;
- every result keeps `authorization: "not_granted"`.

Example:

```bash
python tooling/composer.py examples/composition-request.json
```

The current Product example composes:

```text
product-discovery
  product.discovery-result.v1 / S2
        ↓
feature-specification
  accepts product.discovery-result.v1 / S0,S1,S2
```

See `standards/composition.md`, `standards/handoffs.md`, `schemas/composition-request.schema.json` and `schemas/composition-result.schema.json`.

## Skill lifecycle

```text
DRAFT -> REVIEW -> CANDIDATE -> APPROVED -> ACTIVE -> DEPRECATED -> RETIRED
QUARANTINED = exceptional safety state
```

A runtime may maintain a separate deployment lifecycle such as available, installed, enabled, disabled or quarantined.

## Quality gates

| Gate | Meaning |
|---|---|
| Q0 | Schema |
| Q1 | Static quality |
| Q2 | Scenario tests |
| Q3 | Security / sandbox |
| Q4 | Golden Task execution |
| Q5 | Regression evidence |

Q4 and Q5 require **verified execution evidence**. Definition files alone never count as PASS. CI blocks `approved` or `active` Skills without the required evidence.

### Q4/Q5 evaluation harness

The canonical evidence workflow is:

```text
PREPARE
  -> external EXECUTION
  -> independent VERIFICATION
  -> FINALIZE
  -> evaluator re-validation
```

Low-level preparation:

```bash
python tooling/eval_harness.py prepare \
  skills/agenticos/agenticos-agent-audit \
  --gate Q4
```

The external runner returns sanitized observations. A different human, deterministic verifier or independent model checks the exact expected result, every criterion and every forbidden behavior. Finalize only after that independent verification.

The generated result is bound to Skill ID/version, `package_sha256` and the exact evaluation-definition hash. Editing the Skill or Golden/Regression definition invalidates stale evidence automatically.

### Golden Runtime Qualification Path — AgenticOS

`tooling/qualification.py` implements the governed last mile between Skills Brain evaluation definitions and an external AgenticOS/Hermes execution.

```text
Skills Brain PREPARE
        ↓
request.json + agenticos-plan.json
        ↓
AgenticOS / Hermes execution
        ↓
observation.json
        ↓
Skills Brain COLLECT
        ↓
runner-results.json
        ↓
Independent verifier
        ↓
verification.json
        ↓
Skills Brain FINALIZE
        ↓
golden-results.json / regression-results.json
```

Check the first Golden Path Skill:

```bash
python tooling/qualification.py status \
  skills/engineering/codebase-analysis
```

Prepare its Q4 run:

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

The plan always has:

```json
{"authorization": "not_granted"}
```

AgenticOS must independently authorize the run, use its normal Skills Brain binding and return the exact upstream Skill ID/version/package hash/source commit in `observation.json`.

Collect the runtime observation without scoring it:

```bash
python tooling/qualification.py collect \
  --request /secure/eval/codebase-analysis-q4/request.json \
  --observation /secure/eval/codebase-analysis-q4/observation.json
```

Only after a different verifier has produced `verification.json` may the run be finalized:

```bash
python tooling/qualification.py finalize \
  skills/engineering/codebase-analysis \
  --request /secure/eval/codebase-analysis-q4/request.json \
  --runner-results /secure/eval/codebase-analysis-q4/runner-results.json \
  --verification /secure/eval/codebase-analysis-q4/verification.json
```

A successful AgenticOS worker exit is **not** a Golden Task PASS. The runner adapter never sets semantic score or `verified=true`.

#### Q5 verified baseline

Q5 requires independently measured historical metrics conforming to `schemas/regression-baseline.schema.json`. Naming `codebase-analysis@0.1.0` in `regression.yaml` is not enough to establish historical values.

`qualification.py prepare --gate Q5` fails closed until a verified baseline exists. Synthetic historical metrics are forbidden; the historical version must be measured under a controlled benchmark or Q5 must be deferred.

Generated Q4/Q5 results and `regression-baseline.json` are evaluation evidence and are excluded from `package_sha256`; evaluation **definitions and fixtures remain included**, so changing the benchmark still invalidates stale evidence.

See `standards/evaluation.md`, `standards/runtime-qualification.md` and `adapters/agenticos/README.md`.

## Supply-chain integrity

Skills Brain defines deterministic:

```text
skill_sha256
manifest_sha256
package_sha256
```

`package_sha256` covers all regular source files unless explicitly excluded by `standards/integrity.md`.

```bash
python tooling/integrity.py skills/services/zabbix-proxi-monitor
```

A downstream runtime should pin both the resolved source commit and `package_sha256`, recompute the hash independently and fail closed on mismatch.

## AgenticOS integration

```text
Skills Brain
  -> pinned commit/tag
  -> validate/evaluate/hash
  -> AgenticOS immutable snapshot
  -> local tenant/tool/policy bindings
  -> runtime manifest
  -> Hermes
```

Export the canonical governance contract:

```bash
python adapters/agenticos/export.py \
  skills/services/zabbix-proxi-monitor \
  --repository sramiweb/skills-brain \
  --commit <40-char-commit>
```

The export contains identity, capabilities, logical requirements, governance metadata and hashes. It never grants tenants, MCP connectors, concrete tools, credentials, mounts, network profiles or approvals.

AgenticOS remains responsible for tenant authorization, runtime selection, concrete MCP tools, data-class enforcement, sandbox/network profiles, approvals, secrets, execution, audit and rollback. A typed handoff in Skills Brain does not authorize the runtime payload transfer. Tenant-specific empirical reputation likewise remains local unless separately generalized and governed.

## Deliberation and learning

Reusable debate protocols currently include:

- `strategic-debate-v1`
- `technical-debate-v1`
- `operational-debate-v1`

Verified learning follows:

```text
Outcome
-> Retrospective
-> Improvement Proposal
-> Tests
-> Evaluation
-> Review / Debate
-> Approval
-> Skill vNext
```

Production Skills are never modified directly by unreviewed runtime feedback. Statistical reputation may update from verified outcomes, but it is not a Skill modification and never grants execution authority.

## Core governance Skills

Currently present:

- `skill-creator`
- `skill-reviewer`
- `skill-security-reviewer`
- `skill-evaluator`
- `skill-resolver`
- `skill-composer`
- `skill-deliberator`
- `skill-retrospective`

`skill-resolver` describes the eligibility-first and verified-reputation ranking method implemented by `tooling/resolver.py`. `skill-composer` describes the governed multi-Skill and typed-handoff method implemented by `tooling/composer.py`. Both are advisory and always leave runtime authorization ungranted.

## Klerbot Golden Tenant

Klerbot is the first end-to-end Golden Tenant for the Skills Brain <-> AgenticOS architecture.

The first runtime qualification target is `codebase-analysis@0.1.1` through AgenticOS `klerbot-coder`, using the exact immutable Skill package and its built-in `fixtures/mini-service` Golden Tasks.

Reusable methods remain in generic domains such as market, product, customer, revenue, growth, content, sales, engineering, SRE and databases. `skills/klerbot/` is reserved for non-generic Klerbot context.

## Validation

```bash
pip install -r requirements-dev.txt
./scripts/validate-skills.sh
```

Individual commands:

```bash
python tooling/validate.py --all
pytest -q
python tooling/evaluator.py
python tooling/catalog.py
python tooling/reputation.py --help
python tooling/resolver.py examples/resolution-request.json
python tooling/composer.py examples/composition-request.json
python tooling/eval_harness.py --help
python tooling/qualification.py status skills/engineering/codebase-analysis
```

## Roadmap

| Phase | Objective | Status |
|---|---|---|
| P0 | Canonical structure + duplicate cleanup | Done |
| P1 | Strict v2.1 schema + CI + capability ontology | Done |
| P2 | Evidence-based Q0-Q5 + evaluation harness | Harness + AgenticOS qualification contracts implemented; live external execution/verification pending |
| P3 | Supply-chain integrity + AgenticOS adapter | Governance export + runtime qualification adapter implemented |
| P4 | Catalog + capability resolver/composer | Resolver v1.1 + verified global reputation + deterministic composer with typed handoffs implemented; runtime multi-Skill execution pending |
| P5 | Outcome-driven learning | Foundation + verified reputation aggregation implemented |
| P6 | Deliberation protocols | Foundation done |
| P7 | Additional adapters, explicit transforms and advanced composition | Planned |

See `SPECIFICATION.md` for the normative architecture and rules.

## License

MIT. See `LICENSE`.
