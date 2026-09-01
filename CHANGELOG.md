# Changelog

Tous les changements notables sont documenté««s ici.

Format bas é sur [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### P0 — Nettoyage + Structure v2 (2026-09-01)

#### Added
- `.editorconfig` (UTF-8, LF, no BOM)
- `.gitattributes` (encodage enforce)
- `standards/skill-spec-v2.md` (spé««cification v2)
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
- Quality Gates (Q0-Q5) documenté««es
- Capability Ontology
- Skill Score formula

#### Changed
- `standards/skill-spec-v2.md` → source de vé «rité««
- Lifecycle : DRAFT → REVIEW → CANDIDATE → APPROVED → ACTIVE → DEPRECATED → RETIRED

### P0+P1 — Stats

- **9 skills** migré««s vers v2
- **4 AgenticOS** : deploy, security-scan, migration-runner, agent-audit
- **4 Templates** : deployment, security-audit, migration, eval
- **1 Service** : zabbix-proxi-monitor

### Todo (P2)

- Skill evaluator (golden tasks, scores)
- Skill resolver (capability matching, ranking)
- Catalog generator (index.json, capabilities.json)
- Skill graph (dependencies, composition)

## [1.0.0] - 2026-09-01

### Added
- Initial release
- Structure de base (`templates/`, `agenticos/`, `services/`)
- Documentation complè««te
- CI/CD (`validate-skills.yml`)
- Scripts (`validate-skills.sh`)
