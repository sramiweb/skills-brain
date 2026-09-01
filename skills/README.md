# Skills

Bibliothè««que de skills pour agents IA — structure v2.

## Catégories

| Catégorie | Description | Skills |
|-----------|-------------|--------|
| [`agenticos/`](./agenticos/) | Skills AgenticOS | 4 |
| [`templates/`](./templates/) | Templates gén ériques | 4 |
| [`services/`](./services/) | Services externes | 1 |

## Structure v2

Chaque skill suit la structure :

```
<skill-name>/
├── SKILL.md            # Portable pour agents (frontmatter minimal)
├── skill.yaml          # Métadonné««es machine (Skills Brain)
├── tests/
│   └── scenarios.yaml  # Happy path, edge case, stress case
├── evals/
│   └── golden.yaml     # Tâ««ches de ré «f érence
├── references/         # Documentation externe
└── CHANGELOG.md        # Historique des versions
```

## Standards

- [`standards/skill-spec-v2.md`](../standards/skill-spec-v2.md) — Spé««cification complè««te
- [`standards/security.md`](../standards/security.md) — Security manifest
- [`standards/evaluation.md`](../standards/evaluation.md) — Quality gates

## Qualité

Chaque skill passe par 5 quality gates (Q0-Q5) avant d'ê««tre approuvé««.

Voir [`SPECIFICATION.md`](../SPECIFICATION.md) pour la vision complè««te.
