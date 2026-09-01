# AgenticOS Skills

Skills spécifiques à AgenticOS — implé««mentations réelles des templates gén ériques.

## Skills Disponibles

| Skill | Version | Status | Capabilities |
|-------|---------|--------|-------------|
| [`agenticos-deploy`](./agenticos-deploy/SKILL.md) | 1.0.0 | active | deploy, rollback |
| [`agenticos-security-scan`](./agenticos-security-scan/SKILL.md) | 1.0.0 | active | security, audit |
| [`agenticos-migration-runner`](./agenticos-migration-runner/SKILL.md) | 1.0.0 | active | database, migration |
| [`agenticos-agent-audit`](./agenticos-agent-audit/SKILL.md) | 1.0.0 | active | evaluation, quality |

## Structure (v2)

Chaque skill suit maintenant le format v2 :

```
agenticos-deploy/
├── SKILL.md            # Portable pour agents
├── skill.yaml          # Métadonné««es machine (à«« venir)
├── tests/
│   └── scenarios.yaml  # (à«« venir)
└── evals/
    └── golden.yaml     # (à«« venir)
```

## Migration v1 → v2

Les skills AgenticOS ont é «té«« dé «placé««s de `agenticos/` vers `skills/agenticos/` pour la structure v2.

Voir [`standards/skill-spec-v2.md`](../../standards/skill-spec-v2.md) pour la spé «cification complè««te.
