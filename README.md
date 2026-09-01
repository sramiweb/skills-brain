# Skills Brain v2

> **An open intelligence and governance layer for Agent Skills**
>
> Find, evaluate, compose and govern the right skills for AI agents.

[![Validate Skills](https://github.com/sramiweb/skills-brain/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/sramiweb/skills-brain/actions/workflows/validate-skills.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Vision

**Skills Brain** est une plateforme open source permettant de définir, découvrir, valider, évaluer, sécuriser, composer et faire évoluer des compétences utilisables par des agents IA.

Un Skill n'est pas simplement un prompt.  
Un Skill représente une **capacité«« opérationnelle versionné««e et mesurable**.

## Positionnement

Skills Brain est **indé««pendant** d'AgenticOS et peut ê «tre utilisé par :

- AgenticOS
- Hermes Agent
- Claude Code
- Codex
- OpenCode
- Cursor
- Autres agents compatibles avec SKILL.md

**Skills Brain** = Systè««me de connaissance et gouvernance des compé««tences  
**AgenticOS** = Runtime et orchestrateur

## Architecture

```
skills-brain/
├── standards/              # Règles communes (skill-spec-v2, security, etc.)
├── schemas/                # JSON Schemas (skill.schema.json, etc.)
├── skills/                 # Bibliothèque de skills
│   ├── agenticos/          # Skills AgenticOS
│   ├── templates/          # Templates gén ériques
│   └── services/           # Services externes
├── tooling/                # Outils CLI (validate.py, etc.)
└── .github/workflows/      # CI/CD
```

## Skills Disponibles

### AgenticOS (4 skills)

| Skill | Version | Capabilities |
|-------|---------|-------------|
| [`agenticos-deploy`](./skills/agenticos/agenticos-deploy/SKILL.md) | 1.0.0 | deploy, rollback |
| [`agenticos-security-scan`](./skills/agenticos/agenticos-security-scan/SKILL.md) | 1.0.0 | security, audit |
| [`agenticos-migration-runner`](./skills/agenticos/agenticos-migration-runner/SKILL.md) | 1.0.0 | database, migration |
| [`agenticos-agent-audit`](./skills/agenticos/agenticos-agent-audit/SKILL.md) | 1.0.0 | evaluation, quality |

### Templates (4 skills)

| Template | Version | Description |
|----------|---------|-------------|
| [`template-deployment`](./skills/templates/template-deployment/SKILL.md) | 1.0.0 | Dé «ploiement/rollback |
| [`template-security-audit`](./skills/templates/template-security-audit/SKILL.md) | 1.0.0 | Audit sé «curité«« |
| [`template-migration`](./skills/templates/template-migration/SKILL.md) | 1.0.0 | Migrations DB |
| [`template-eval`](./skills/templates/template-eval/SKILL.md) | 1.0.0 | É «valuation qualité «|

### Services Externes (1 skill)

| Skill | Version | External |
|-------|---------|----------|
| [`zabbix-proxi-monitor`](./skills/services/zabbix-proxi-monitor/SKILL.md) | 1.0.0 | Zabbix |

## Démarrage

### Validation

```bash
# Valider tous les skills
python tooling/validate.py --all

# Valider un skill spécifique
python tooling/validate.py skills/agenticos/agenticos-deploy
```

### Structure d'un Skill v2

```
<skill-name>/
├── SKILL.md            # Portable pour agents (frontmatter minimal)
├── skill.yaml          # Métadonné««es machine (Skills Brain)
├── tests/
│   └── scenarios.yaml  # Happy path, edge case, stress case
├── evals/
│   └── golden.yaml     # Tâ««ches de ré «f érence
└── CHANGELOG.md
```

## Standards

- [`standards/skill-spec-v2.md`](./standards/skill-spec-v2.md) — Spé««cification complè««te
- [`schemas/skill.schema.json`](./schemas/skill.schema.json) — JSON Schema v2

## Quality Gates

| Gate | Description |
|------|-------------|
| Q0 | Schema (frontmatter, skill.yaml, format, encoding) |
| Q1 | Static (scope, dependencies, permissions, security) |
| Q2 | Scenario (happy path, edge case, stress case) |
| Q3 | Sandbox (exé««cution sans effet dangereux) |
| Q4 | Golden Tasks (ré««sultats comparé««s aux attentes) |
| Q5 | Regression (comparaison old vs candidate) |

## Principes

- **Don't create a Skill when one already exists**
- **Don't trust a Skill before evaluating it**
- **Don't activate a Skill before governing it**
- **Don't duplicate a Skill when composition works**
- **Don't improve a Skill without measuring regression**

## Roadmap

| Phase | Objectif | Statut |
|-------|----------|--------|
| P0 | Nettoyage + Structure v2 | ✅ |
| P1 | Skill Spec v2 + Schemas + Tooling | ✅ |
| P2 | Quality (evaluator, golden tasks, scores) | ⏳ |
| P3 | Intelligence (catalog, resolver, graph) | ⏳ |
| P4 | Composition (DAG, composite skills) | ⏳ |
| P5 | Deliberation (council, debate, decision) | ⏳ |

## Contribution

1. Fork le dé «pô«««
2. Cr é er une branche (`feature/mon-skill`)
3. Suivre [`standards/skill-spec-v2.md`](./standards/skill-spec-v2.md)
4. Ajouter tests + documentation
5. Valider : `python tooling/validate.py --all`
6. Ouvrir une Pull Request

## License

MIT — Voir [`LICENSE`](./LICENSE).

## Contact

- **Author** : S R
- **Email** : 122878753+sramiweb@users.noreply.github.com
- **Repo** : https://github.com/sramiweb/skills-brain
