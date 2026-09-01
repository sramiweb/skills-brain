# Templates

Templates gén ériques pour workflows communs — bases pour les skills spécifiques.

## Templates Disponibles

| Template | Version | Description |
|----------|---------|-------------|
| [`template-deployment`](./template-deployment/SKILL.md) | 1.0.0 | Dé «ploiement/rollback |
| [`template-security-audit`](./template-security-audit/SKILL.md) | 1.0.0 | Audit sé «curité«« |
| [`template-migration`](./template-migration/SKILL.md) | 1.0.0 | Migrations DB |
| [`template-eval`](./template-eval/SKILL.md) | 1.0.0 | É «valuation qualité «|

## Usage

Les templates sont des skills gén ériques qui doivent ê «tre impl é menté««s par des skills spécifiques :

- `template-deployment` → `agenticos-deploy`
- `template-security-audit` → `agenticos-security-scan`
- `template-migration` → `agenticos-migration-runner`
- `template-eval` → `agenticos-agent-audit`

## Structure

Chaque template suit le format standard :

```
template-deployment/
└── SKILL.md
```

Voir [`standards/skill-spec-v2.md`](../../standards/skill-spec-v2.md).
