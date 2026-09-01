# Skills Brain v2.1

> **Open Skill Intelligence & Governance Plane for AI agents**

Skills Brain defines, evaluates, governs, composes and evolves reusable Agent Skills.

It is intentionally independent from any single runtime.

## Positioning

```text
Skills Brain = canonical skills, protocols, evaluation and reusable knowledge
AgenticOS    = orchestration, runtime bindings, policy, approvals and execution authority
Hermes       = agentic reasoning and execution runtime
MCP          = tools and actions
LiteLLM      = model routing gateway
```

A Skill describes **how to perform a capability**. It does not grant itself runtime permissions.

## Core principles

- Skills are portable and versioned.
- AgenticOS-specific tenant bindings do not belong in canonical Skills.
- Evidence is required before trust.
- Security and policy are fail-closed.
- Debate preserves dissent and does not rely on naive majority voting.
- Runtime outcomes may generate learning and improvement proposals, but never uncontrolled production self-modification.
- A small set of evaluated Skills is more valuable than a large unmeasured catalog.

## Repository architecture

```text
skills-brain/
├── standards/          # Normative rules: lifecycle, security, deliberation, learning...
├── schemas/            # Machine contracts
├── core/               # Meta-skills: creator, reviewer, evaluator, resolver...
├── skills/             # Canonical skill packages
├── protocols/          # Debate, review, red-team, consensus, approval protocols
├── catalog/            # Generated indexes and capability maps
├── adapters/           # Runtime/platform adapters
├── tooling/            # Validation, catalog, evaluation, resolver tooling
├── evaluations/        # Cross-skill evaluation assets
├── tests/              # Tooling/schema/protocol tests
└── .github/workflows/  # CI
```

Some directories are being introduced progressively during the v2.1 migration.

## Skill package

New canonical Skills use `schema_version: "2.1"`.

```text
<skill>/
├── SKILL.md
├── skill.yaml
├── README.md
├── CHANGELOG.md
├── tests/
│   ├── scenarios.yaml
│   └── negative.yaml
├── evals/
│   ├── golden.yaml
│   └── regression.yaml
└── references/
```

Existing `2.0` manifests remain temporarily supported through `schemas/skill-v2.0.schema.json`. New Skills must target the strict `schemas/skill.schema.json` v2.1 contract.

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

A runtime may have a separate deployment state such as available, installed, enabled, disabled or quarantined.

## Quality gates

The canonical quality gates are:

| Gate | Meaning |
|---|---|
| Q0 | Schema |
| Q1 | Static quality |
| Q2 | Scenario tests |
| Q3 | Security / sandbox |
| Q4 | Golden tasks |
| Q5 | Regression |

The same Q0-Q5 definitions must be used by the specification, evaluator, CLI and CI.

## Deliberation

Skills Brain now defines reusable deliberation protocols.

Initial protocols:

- `strategic-debate-v1`
- `technical-debate-v1`
- `operational-debate-v1`

Canonical debate properties include:

- independent blind first round;
- evidence-backed arguments;
- cross-examination;
- revised positions;
- preserved dissent;
- independent judgement;
- security veto;
- bounded rounds/cost;
- human approval when runtime policy requires it.

See `standards/deliberation.md` and `protocols/debate/`.

## Learning

Skills Brain distinguishes memory from learning.

```text
SIGNAL
  -> PATTERN
  -> HYPOTHESIS
  -> VERIFIED LEARNING
  -> OPERATIONALIZED KNOWLEDGE
```

Runtime systems such as AgenticOS may submit privacy-preserving outcome and learning signals. Reusable improvements follow:

```text
Outcome
  -> Retrospective
  -> Learning
  -> Improvement Proposal
  -> Tests
  -> Evaluation
  -> Review / Debate
  -> Approval
  -> Skill vNext
```

Canonical Skills are never modified directly by unreviewed runtime feedback.

See `standards/learning.md` and the outcome/learning/improvement schemas.

## AgenticOS integration

Skills Brain is the upstream source of truth. AgenticOS should consume only validated immutable snapshots.

```text
Skills Brain
  -> pinned tag/commit
  -> validate/evaluate
  -> AgenticOS install snapshot
  -> local bindings/policies
  -> runtime manifest
  -> Hermes
```

AgenticOS remains responsible for:

- tenant authorization;
- runtime selection;
- MCP connectors/tools;
- data classification enforcement;
- sandbox/network profiles;
- approvals;
- secrets;
- execution and rollback.

Never let a runtime agent pull and execute `main` directly during a mission.

## Klerbot Golden Tenant

Klerbot is the first end-to-end Golden Tenant for the Skills Brain <-> AgenticOS architecture.

`skills/klerbot/` contains Klerbot-specific context knowledge only. Generic methods remain in generic domains such as market, product, customer, revenue, growth, content, sales, engineering, SRE and security.

## Validation

Install development dependencies explicitly:

```bash
pip install -r requirements-dev.txt
```

Validate all canonical Skills:

```bash
python tooling/validate.py --all
```

Run the full test suite:

```bash
pytest -q
```

Generate the catalog:

```bash
python tooling/catalog.py
```

## Security

Canonical Skills may declare requirements and constraints, but Skills Brain does not grant runtime authority. Effective permissions must be computed by the consuming runtime from the intersection of Skill requirements, runtime bindings, tenant policy and tool policy.

A quarantined Skill must not be selected, installed or newly activated by a compliant runtime.

## Roadmap

| Phase | Objective | Status |
|---|---|---|
| P0 | Canonical structure + schema migration | In progress |
| P1 | Real CI + evaluation + golden tasks | In progress |
| P2 | Catalog + capability ontology + resolver | Planned |
| P3 | Deliberation protocols | In progress |
| P4 | Outcome-driven learning + improvement governance | In progress |
| P5 | Composition + advanced resolution | Planned |
| P6 | Runtime adapters + reputation | Planned |

## License

MIT. See `LICENSE`.
