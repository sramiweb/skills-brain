# AgenticOS Skills

Skills spécifiques à AgenticOS — implé««mentations réelles des templates gén ériques.

## Skills à Créer (Phase 1)

| Skill | Template Source | Description |
|-------|-----------------|-------------|
| `agenticos-deploy` | `template-deployment` | Dé «ploiement réel sur AgenticOS |
| `agenticos-security-scan` | `template-security-audit` | Audit sé «curité«« AgenticOS |
| `agenticos-migration-runner` | `template-migration` | Exé««cution migrations AgenticOS |
| `agenticos-agent-audit` | `template-eval` | É «valuation qualité «| `evaluate` |

## Structure

Chaque skill AgenticOS suit le même format que les templates :

```
agenticos/
├── README.md
├── agenticos-deploy/
│   └── SKILL.md
├── agenticos-security-scan/
│   └── SKILL.md
├── agenticos-migration-runner/
│   └── SKILL.md
└── agenticos-agent-audit/
    └── SKILL.md
```

## Prochaines É «tapes

1. Créer `agenticos-deploy` (ré««fé««rence : `templates/template-deployment`)
2. Créer `agenticos-security-scan`
3. Créer `agenticos-migration-runner`
4. Créer `agenticos-agent-audit`

Voir [`SPECIFICATION.md`](../SPECIFICATION.md) pour les standards de qualité «.
