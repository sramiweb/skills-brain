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
- Composition plans requirements; it never grants runtime permissions.
- Runtime outcomes may produce improvement proposals, never uncontrolled production self-modification.
- A small set of evaluated Skills is more valuable than a large unmeasured catalog.

## Repository architecture

```text
skills-brain/
├── standards/          # Normative lifecycle, capabilities, evaluation, resolution, composition, integrity, deliberation, learning
├── schemas/            # Machine contracts
├── core/               # Governance meta-skills
├── skills/             # Canonical skill packages
├── protocols/          # Debate and decision protocols
├── catalog/            # Generated indexes
├── adapters/           # Runtime/platform export contracts
├── tooling/            # Validation, evaluation, catalog, resolver, composer and integrity tooling
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

Optional source assets include `README.md`, `CHANGELOG.md`, `tests/`, `evals/`, `references/`, `resources/`, `scripts/` and `fixtures/`.

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

A high quality score cannot override a missing tool, incompatible data class or denied lifecycle state.

The resolver returns:

```json
{"authorization": "not_granted"}
```

Example:

```bash
python tooling/resolver.py examples/resolution-request.json
```

The v1 ranking uses capability coverage, measured Q0-Q5 quality, lifecycle maturity and risk fitness. Missing evaluation evidence contributes zero. `minimum_score` is a threshold and is never treated as achieved quality.

See `standards/resolution.md` and `schemas/resolution-request.schema.json`.

## Governed Skill composer

`tooling/composer.py` builds a deterministic minimum sufficient plan when multiple capabilities are requested.

```text
requested capabilities
-> resolver-grade eligibility
-> minimum sufficient Skill set
-> transitive dependency closure
-> dependency eligibility
-> conflicts / supersession
-> topological order
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
- the union of `tool_capabilities` is planning information only, never granted permissions;
- quality is used only after eligibility and cannot bypass a rejection;
- every result keeps `authorization: "not_granted"`.

Example:

```bash
python tooling/composer.py examples/composition-request.json
```

See `standards/composition.md`, `schemas/composition-request.schema.json` and `schemas/composition-result.schema.json`.

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

Prepare a content-addressed Golden Task run:

```bash
python tooling/eval_harness.py prepare \
  skills/agenticos/agenticos-agent-audit \
  --gate Q4
```

The external runner returns sanitized observations. A different human, deterministic verifier or independent model checks the exact expected result, every criterion and every forbidden behavior. Finalize only after that independent verification:

```bash
python tooling/eval_harness.py finalize \
  skills/agenticos/agenticos-agent-audit \
  --request reports/eval-runs/agenticos-agent-audit/<run>/request.json \
  --runner-results /secure/path/runner-results.json \
  --verification /secure/path/verification.json
```

The generated result is bound to Skill ID/version, `package_sha256` and the exact evaluation-definition hash. Editing the Skill or Golden/Regression definition invalidates stale evidence automatically.

See `standards/evaluation.md` and the `schemas/eval-*.json` contracts.

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

AgenticOS remains responsible for tenant authorization, runtime selection, concrete MCP tools, data-class enforcement, sandbox/network profiles, approvals, secrets, execution, audit and rollback.

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

Production Skills are never modified directly by unreviewed runtime feedback.

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

`skill-resolver` describes the eligibility-first method implemented by `tooling/resolver.py`. `skill-composer` describes the governed multi-Skill method implemented by `tooling/composer.py`. Both are advisory and always leave runtime authorization ungranted.

## Klerbot Golden Tenant

Klerbot is the first end-to-end Golden Tenant for the Skills Brain <-> AgenticOS architecture.

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
python tooling/resolver.py examples/resolution-request.json
python tooling/composer.py examples/composition-request.json
python tooling/eval_harness.py --help
```

## Roadmap

| Phase | Objective | Status |
|---|---|---|
| P0 | Canonical structure + duplicate cleanup | Done |
| P1 | Strict v2.1 schema + CI + capability ontology | Done |
| P2 | Evidence-based Q0-Q5 + evaluation harness | Harness implemented; external runtime qualification in progress |
| P3 | Supply-chain integrity + AgenticOS adapter | Done |
| P4 | Catalog + capability resolver/composer | Resolver v1 + deterministic composer v1 implemented; runtime multi-Skill execution pending |
| P5 | Outcome-driven learning | Foundation done |
| P6 | Deliberation protocols | Foundation done |
| P7 | Reputation, typed handoffs, additional adapters and advanced composition | Planned |

See `SPECIFICATION.md` for the normative architecture and rules.

## License

MIT. See `LICENSE`.
