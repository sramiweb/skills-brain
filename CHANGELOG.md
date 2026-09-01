# Changelog

Tous les changements notables sont documentes ici.

Format base sur [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### P2 — Tooling Complet + CLI Unifie (2026-09-01)

#### Added
- `tooling/cli.py` — CLI unifiee (`validate`, `catalog`, `evaluate`, `resolve`, `run-all`)
- `tooling/catalog.py` — Generation du catalog (index.json, capabilities.json, dependencies.json)
- `tooling/evaluator.py` — Evaluation skills avec Q0-Q5, scores de qualite
- `tooling/resolver.py` — Matching capabilities + ranking skills
- `reports/` directory — Rapports d'evaluation
- `catalog/` directory — Catalog genere

#### Changed
- Pipeline complet : validate → catalog → evaluate → resolve
- CLI unique pour tous les outils

### P0 — Nettoyage + Structure v2 (2026-09-01)

#### Added
- `.editorconfig` (UTF-8, LF, no BOM)
- `.gitattributes` (encodage enforce)
- `standards/skill-spec-v2.md` (specification v2)
- `skills/` directory avec structure v2 :
  - `skills/agenticos/` (4 skills)
  - `skills/templates/` (4 skills)
  - `skills/services/` (1 skill)
- `skills/README.md`, `skills/agenticos/README.md`, `skills/templates/README.md`, `skills/services/README.md`

#### Changed
- Migration de tous les skills vers `skills/` (nouvelle structure)
- `README.md` → vision Skills Brain v2
- `SPECIFICATION.md` → architecture cible v2

### P1 — Skill Spec v2 + Schemas + Tooling (2026-09-01)

#### Added
- `schemas/skill.schema.json` (JSON Schema v2 pour skill.yaml)
- `tooling/validate.py` (CLI de validation)
- Quality Gates (Q0-Q5) documentees
- Capability Ontology
- Skill Score formula

#### Changed
- `standards/skill-spec-v2.md` → source de verite
- Lifecycle : DRAFT → REVIEW → CANDIDATE → APPROVED → ACTIVE → DEPRECATED → RETIRED

### P0+P1 — Stats

- **9 skills** migres vers v2
- **4 AgenticOS** : deploy, security-scan, migration-runner, agent-audit
- **4 Templates** : deployment, security-audit, migration, eval
- **1 Service** : zabbix-proxi-monitor

## [1.0.0] - 2026-09-01

### Added
- Initial release
- Structure de base (`templates/`, `agenticos/`, `services/`)
- Documentation complete
- CI/CD (`validate-skills.yml`)
- Scripts (`validate-skills.sh`)
