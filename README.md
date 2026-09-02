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

- Skills are portable, versioned and identified canonically.
- Canonical Skills use logical capabilities rather than vendor-specific runtime bindings.
- AgenticOS-specific tenants, connectors, credentials and tool permissions do not belong in canonical Skills.
- Evidence is required before trust.
- Security, compatibility and integrity checks are fail-closed.
- Debate preserves dissent and does not rely on naive majority voting.
- Runtime outcomes may produce improvement proposals, never uncontrolled production self-modification.
- A small set of evaluated Skills is more valuable than a large unmeasured catalog.

## Repository architecture

```text
skills-brain/
├── standards/          # Normative lifecycle, capabilities, integrity, deliberation, learning
├── schemas/            # Machine contracts
├── core/               # Governance meta-skills
├── skills/             # Canonical skill packages (single source location)
├── protocols/          # Debate and decision protocols
├── catalog/            # Generated indexes
├── adapters/           # Runtime/platform export contracts
├── tooling/            # Validation, evaluation, catalog and integrity tooling
├── tests/              # Repository/tooling tests
└── .github/workflows/  # CI
```

Legacy duplicate Skill roots have been removed. `skills/` is the only canonical package location.

## Skill package

New canonical Skills use `schema_version: "2.1"` and the strict `schemas/skill.schema.json` contract.

Minimum package:

```text
<skill>/
├── SKILL.md
└── skill.yaml
```

Optional source assets include `README.md`, `CHANGELOG.md`, `tests/`, `evals/`, `references/`, `resources/`, `scripts/` and `fixtures/`.

The v2.0 schema remains only as a compatibility/migration contract for historical manifests. New Skills must use v2.1.

## Capability ontology

`standards/capabilities.yaml` is the machine-readable ontology for Skill capabilities and logical tool capabilities.

Examples:

```text
product.discover
sales.lead.qualify
engineering.code.review
sre.application.health
database.postgres.diagnose
```

Logical tool requirements such as `filesystem.read`, `logs.read` or `monitoring.read` are mapped by the consuming runtime to concrete tools. Skills Brain does not perform that binding.

## Skill lifecycle

```text
DRAFT
  -> REVIEW
  -> CANDIDATE
  -> APPROVED
  -> ACTIVE
  -> DEPRECATED
  -> RETIRED

QUARANTINED = exceptional safety state
```

A runtime may maintain a separate deployment lifecycle such as available, installed, enabled, disabled or quarantined.

## Quality gates

The canonical gates are:

| Gate | Meaning |
|---|---|
| Q0 | Schema |
| Q1 | Static quality |
| Q2 | Scenario tests |
| Q3 | Security / sandbox |
| Q4 | Golden tasks |
| Q5 | Regression |

Q4 and Q5 require **verified execution evidence**. Definition files alone never count as PASS. CI blocks `approved` or `active` Skills that do not satisfy required evidence gates.

## Supply-chain integrity

Skills Brain defines deterministic:

```text
skill_sha256
manifest_sha256
package_sha256
```

`package_sha256` covers all regular source files in a Skill package unless explicitly excluded by `standards/integrity.md`. New directories such as `scripts/`, `resources/` or `assets/` are therefore covered automatically.

A downstream runtime should pin both the resolved source commit and `package_sha256`, recompute the hash independently and fail closed on mismatch.

Calculate hashes locally:

```bash
python tooling/integrity.py skills/services/zabbix-proxi-monitor
```

## AgenticOS integration

Skills Brain is the upstream source of canonical knowledge. AgenticOS consumes validated immutable snapshots and applies local bindings.

```text
Skills Brain
  -> pinned commit/tag
  -> validate/evaluate/hash
  -> AgenticOS immutable snapshot
  -> local tenant/tool/policy bindings
  -> runtime manifest
  -> Hermes
```

The AgenticOS adapter exports a governance contract:

```bash
python adapters/agenticos/export.py \
  skills/services/zabbix-proxi-monitor \
  --repository sramiweb/skills-brain \
  --commit <40-char-commit>
```

The export contains canonical identity, capabilities, requirements, governance metadata and hashes. It never grants tenants, MCP connectors, concrete tools, credentials, mounts, network profiles or approval decisions.

AgenticOS remains responsible for:

- tenant authorization;
- runtime selection;
- MCP connectors and concrete tools;
- data-class enforcement;
- sandbox/network profiles;
- approvals;
- credentials and secrets;
- execution, audit and rollback.

Never let a runtime worker pull and execute a floating `main` during a mission.

## Deliberation

Initial reusable debate protocols:

- `strategic-debate-v1`
- `technical-debate-v1`
- `operational-debate-v1`

They use independent first-round positions, evidence, cross-examination, preserved dissent, independent judgement, security veto and bounded cost/rounds. See `standards/deliberation.md` and `protocols/debate/`.

## Learning

Skills Brain distinguishes memory from verified learning.

```text
SIGNAL
  -> PATTERN
  -> HYPOTHESIS
  -> VERIFIED LEARNING
  -> OPERATIONALIZED KNOWLEDGE
```

Reusable improvements follow a governed loop:

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

Canonical production Skills are never modified directly by unreviewed runtime feedback.

## Core governance Skills

Currently present:

- `skill-creator`
- `skill-reviewer`
- `skill-evaluator`
- `skill-deliberator`
- `skill-retrospective`

Advanced resolver, composition and specialized security review remain future work.

## Klerbot Golden Tenant

Klerbot is the first end-to-end Golden Tenant used to validate the Skills Brain <-> AgenticOS architecture.

Generic methods remain in reusable domains such as market, product, customer, revenue, growth, content, sales, engineering, SRE and databases. `skills/klerbot/` is reserved for Klerbot-specific context that is not reusable as a generic Skill.

## Validation

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the canonical local validation pipeline:

```bash
./scripts/validate-skills.sh
```

Or run individual steps:

```bash
python tooling/validate.py --all
pytest -q
python tooling/evaluator.py
python tooling/catalog.py
```

CI additionally hashes every canonical Skill and blocks promoted Skills without required evidence.

## Roadmap

| Phase | Objective | Status |
|---|---|---|
| P0 | Canonical structure + duplicate cleanup | Done |
| P1 | Strict v2.1 schema + CI + capability ontology | Done |
| P2 | Evidence-based Q0-Q5 + execution harness | In progress |
| P3 | Supply-chain integrity + AgenticOS adapter | In progress / advanced |
| P4 | Catalog + intelligent resolver | Catalog done; resolver planned |
| P5 | Outcome-driven learning | Foundation done |
| P6 | Deliberation protocols | Foundation done |
| P7 | Composition, reputation, additional adapters | Planned |

See `SPECIFICATION.md` for the normative architecture and rules.

## License

MIT. See `LICENSE`.
