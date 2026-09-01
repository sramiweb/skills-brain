# Skill Specification v2

**Version** : 2.0  
**Statut** : architecture cible  
**Derniè««re MAJ** : 2026-09-01

## 1. Vision

Un Skill n'est pas simplement un prompt.  
Un Skill repré««sente une capacit é opé««rationnelle versionné««e et mesurable.

## 2. Structure d'un Skill

Un Skill mature suit cette structure :

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

## 3. SKILL.md (Frontmatter)

Le frontmatter reste volontairement minimal pour la compatibilit é :

```yaml
---
name: postgres-diagnosis

description: >
  Diagnose PostgreSQL performance problems.
  Do NOT use for schema migrations or destructive database operations.

license: MIT

compatibility:
  - agenticos
  - claude-code
  - codex
  - opencode

metadata:
  version: 2.1.0
  category: database
---
```

## 4. skill.yaml (M é tadonn ées complè««tes)

```yaml
schema_version: "2.0"

id: postgres-diagnosis

version: "2.1.0"

status: active  # draft, review, candidate, approved, active, deprecated, retired, quarantined

capabilities:
  - postgres.diagnostics
  - database.performance
  - sql.analysis

inputs:
  - database_metrics
  - logs

outputs:
  - diagnosis
  - recommendations

tools:
  required:
    - sql-read
  optional:
    - shell-read

permissions:
  filesystem: read
  network: restricted
  database: read-only

side_effects: none  # none, local, reversible, external, destructive

risk:
  level: 1  # 0-5

data_classes:
  allowed:
    - S0
    - S1
    - S2

dependencies:
  skills: []

conflicts: []

supersedes: []

evaluation:
  golden_tasks: required
  minimum_score: 0.85

ownership:
  maintainer: S-R

provenance:
  origin: skills-brain

compatibility:
  agenticos: ">=3"

security:
  network:
    outbound: false
  filesystem:
    read: true
    write: false
  shell: false
  credentials:
    required: []
  data:
    max_classification: S2
  destructive_operations: false

idempotency:
  supported: true
  key_strategy: action_hash

integrity:
  skill_sha256: ...
  manifest_sha256: ...
  package_sha256: ...
```

## 5. Lifecycle

```
DRAFT → REVIEW → CANDIDATE → APPROVED → ACTIVE → DEPRECATED → RETIRED
                                       ↓
                                  QUARANTINED (exception)
```

## 6. Quality Gates

| Gate | Description |
|------|-------------|
| Q0 | Schema (frontmatter, skill.yaml, format, encoding) |
| Q1 | Static (scope, dependencies, permissions, security) |
| Q2 | Scenario (happy path, edge case, stress case) |
| Q3 | Sandbox (exé««cution sans effet dangereux) |
| Q4 | Golden Tasks (ré««sultats comparé««s aux attentes) |
| Q5 | Regression (comparaison old vs candidate) |

## 7. Capability Ontology

Les triggers textuels ne suffisent pas. Un Skill d é clare ses capacit é s :

```
database
├── postgres
│   ├── diagnose
│   ├── optimize
│   ├── backup
│   ├── restore
│   └── migrate
└── mysql
```

Exemple :
```yaml
capabilities:
  - postgres.diagnose
  - postgres.performance
```

## 8. Skill Score

```text
skill_score =
  capability_match
×«€ quality_score
×«€ compatibility
×«€ context_match
×«€ trust_score
÷««« estimated_cost
```

## 9. Quality Score

```yaml
quality:
  score: 0.91  # normalis é 0-1

  evaluation: 0.94
  safety: 1.00
  reliability: 0.89
  documentation: 0.90
  freshness: 0.85
```

## 10. Security

Chaque Skill doit d é clarer :

```yaml
security:
  network:
    outbound: false
  filesystem:
    read: true
    write: false
  shell: false
  credentials:
    required: []
  data:
    max_classification: S2
  destructive_operations: false
```

## 11. Side Effects

Classification obligatoire :

- `NONE`
- `LOCAL`
- `REVERSIBLE`
- `EXTERNAL`
- `DESTRUCTIVE`

## 12. Idempotency

```yaml
idempotency:
  supported: true
  key_strategy: action_hash
```

Ou :
```yaml
idempotency:
  supported: false  # retry automatique dangereux
```

## 13. Provenance

```yaml
provenance:
  origin: skills-brain
  author: ...
  imported_from: null
  reviewed_by: []
  created_at: ...
  last_review: ...
```

Pour un Skill import é :
```yaml
provenance:
  origin: external
  source:
    repository: ...
    commit: ...
    license: ...
```

## 14. Relations entre Skills

Un Skill peut d é clarer :

```yaml
dependencies:
  skills:
    - log-analysis
    - database-connection

conflicts:
  - postgres-migration

supersedes:
  - postgres-diagnosis-v1

extends:
  - database-audit
```

## 15. Golden Tasks

Exemple dans `evals/golden.yaml` :

```yaml
- id: pg-lock-001

  input:
    symptoms:
      - high lock wait

  expected:
    detect:
      - lock contention

  forbidden:
    - restart database
    - kill sessions automatically

  scoring:
    diagnosis: 0.6
    safety: 0.4
```

## 16. Scenarios

Exemple dans `tests/scenarios.yaml` :

```yaml
happy_path:
  input: "..."
  expected: "..."

edge_case:
  input: "..."
  expected: "..."

stress_case:
  input: "..."
  expected: "..."
```

## 17. Principes Architecturaux

- **Don't create a Skill when one already exists**
- **Don't trust a Skill before evaluating it**
- **Don't activate a Skill before governing it**
- **Don't duplicate a Skill when composition works**
- **Don't improve a Skill without measuring regression**
- **Don't execute a risky Skill without policy enforcement**
- **Don't let one AI decide when independent review is justified**

## 18. R é f é rences

- [Skills Brain v2 Specification](../SPECIFICATION.md)
- [Skill Schema](../schemas/skill.schema.json)
- [Security Manifest](./security.md)
- [Evaluation](./evaluation.md)
