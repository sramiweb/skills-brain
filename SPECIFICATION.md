# Skills Brain v2 — Spé««cifications

**Version** : 2.0  
**Statut** : architecture cible  
**Derniè««re MAJ** : 2026-09-01

## 1. Vision

**Skills Brain** est une plateforme open source permettant de définir, découvrir, valider, évaluer, sécuriser, composer et faire évoluer des compétences utilisables par des agents IA.

Un Skill n'est pas simplement un prompt.  
Un Skill représente une **capacité«« opérationnelle versionné««e et mesurable**.

## 2. Positionnement

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

## 3. Architecture Cible

```
skills-brain/
│
├── README.md                 # Vue d'ensemble
├── SPECIFICATION.md          # Ce fichier
├── LICENSE                   # MIT
├── CHANGELOG.md              # Historique
│
├── standards/                # Règles communes
│   ├── skill-spec-v2.md      # Spé««cification Skill
│   ├── lifecycle.md          # Lifecycle (draft → retired)
│   ├── security.md           # Security manifest
│   ├── evaluation.md         # Quality gates
│   ├── compatibility.md      # Compatibilité«« agents
│   └── composition.md        # Composition de skills
│
├── schemas/                  # JSON Schemas
│   ├── skill.schema.json     # skill.yaml
│   ├── test.schema.json      # tests/scenarios.yaml
│   ├── eval.schema.json      # evals/golden.yaml
│   ├── decision.schema.json  # decision records
│   └── capability.schema.json# Capability ontology
│
├── core/                     # Composants core (à«« venir)
│   ├── skill-creator/
│   ├── skill-reviewer/
│   ├── skill-evaluator/
│   ├── skill-resolver/
│   ├── skill-composer/
│   ├── skill-security-reviewer/
│   ├── skill-deliberator/
│   └── skill-retrospective/
│
├── skills/                   # Bibliothèque de skills
│   ├── agenticos/            # Skills AgenticOS
│   ├── templates/            # Templates gén ériques
│   └── services/             # Services externes
│
├── protocols/                # Protocoles (à«« venir)
│   ├── review/
│   ├── debate/
│   ├── red-team/
│   ├── consensus/
│   └── human-approval/
│
├── catalog/                  # Catalog (à«« venir)
│   ├── index.json
│   ├── capabilities.json
│   ├── dependencies.json
│   └── compatibility.json
│
├── adapters/                 # Adapters (à«« venir)
│   ├── agenticos/
│   ├── claude-code/
│   ├── codex/
│   ├── opencode/
│   └── cursor/
│
├── tooling/                  # Outils CLI
│   ├── validate.py           # Validation skills
│   ├── catalog.py            # Géné «ration catalog
│   ├── resolve.py            # Skill resolver
│   ├── eval.py               # É «valuation
│   └── graph.py              # Skill graph
│
├── tests/                    # Tests du repository
│
└── .github/
    └── workflows/
        └── skills-ci.yml     # CI/CD
```

## 4. Responsabilit é s

Skills Brain doit ré «pondre à «€ sept questions fondamentales :

1. **Quel Skill existe ?** — Catalog + Discovery
2. **Quel Skill correspond le mieux à «€ cette mission ?** — Resolver + Ranking
3. **Ce Skill est-il sû «€r ?** — Security Reviewer + Policies
4. **Ce Skill fonctionne-t-il ré «€llement ?** — Evaluator + Tests
5. **Avec quels agents/outils est-il compatible ?** — Compatibility Matrix
6. **Existe-t-il un meilleur Skill ?** — Quality Score + Reputation
7. **Que devons-nous am é liorer aprè««s son utilisation ?** — Retrospective + Feedback

## 5. Skill Structure v2

```
<skill-name>/
│
├── SKILL.md            # Portable pour agents (frontmatter minimal)
├── skill.yaml          # Mé «tadonn ées machine (Skills Brain)
│
├── tests/
│   └── scenarios.yaml  # Happy path, edge case, stress case
│
├── evals/
│   └── golden.yaml     # Tâ««ches de ré «f érence
│
├── references/         # Documentation externe
│
└── CHANGELOG.md        # Historique des versions
```

## 6. Lifecycle

```
DRAFT → REVIEW → CANDIDATE → APPROVED → ACTIVE → DEPRECATED → RETIRED
                                       ↓
                                  QUARANTINED (exception)
```

Aucun auto-publish : un agent ne peut jamais faire `CANDIDATE → ACTIVE` automatiquement pour un Skill avec side effects significatifs.

## 7. Quality Gates

| Gate | Description |
|------|-------------|
| Q0 | Schema (frontmatter, skill.yaml, format, encoding) |
| Q1 | Static (scope, dependencies, permissions, security) |
| Q2 | Scenario (happy path, edge case, stress case) |
| Q3 | Sandbox (exé««cution sans effet dangereux) |
| Q4 | Golden Tasks (ré««sultats comparé««s aux attentes) |
| Q5 | Regression (comparaison old vs candidate) |

## 8. Skill Score

```
skill_score =
  capability_match
×«€ quality_score
×«€ compatibility
×«€ context_match
×«€ trust_score
÷««« estimated_cost
```

## 9. Principes Architecturaux

- **Don't create a Skill when one already exists**
- **Don't trust a Skill before evaluating it**
- **Don't activate a Skill before governing it**
- **Don't duplicate a Skill when composition works**
- **Don't improve a Skill without measuring regression**
- **Don't execute a risky Skill without policy enforcement**
- **Don't let one AI decide when independent review is justified**

## 10. Roadmap

| Phase | Objectif | Statut |
|-------|----------|--------|
| P0 | Nettoyage + Structure v2 | ✅ |
| P1 | Skill Spec v2 + Schemas + Tooling | ✅ |
| P2 | Quality (evaluator, golden tasks, scores) | ⏳ |
| P3 | Intelligence (catalog, resolver, graph) | ⏳ |
| P4 | Composition (DAG, composite skills) | ⏳ |
| P5 | Deliberation (council, debate, decision) | ⏳ |

## 11. R é f é rences

- [`standards/skill-spec-v2.md`](./standards/skill-spec-v2.md)
- [`schemas/skill.schema.json`](./schemas/skill.schema.json)
- [`README.md`](./README.md)
