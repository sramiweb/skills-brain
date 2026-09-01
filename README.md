# Skills-Brain

> Bibliothèque de skills réutilisables pour agents AI (OpenCode, Claude Code, etc.)

## Vision

Fournir des workflows autonomes, testé««s et documenté««s que les agents AI peuvent exé««cuter pour accomplir des tâches spécifiques (dé««ploiement, audit sé «curité««, migration, é «valuation, etc.).

## Démarrage Rapide

### Prérequis

- Agent AI compatible (OpenCode, Claude Code, etc.)
- Accès au dépôt `sramiweb/skills-brain`

### Installation

```bash
git clone https://github.com/sramiweb/skills-brain.git
cd skills-brain
```

### Usage

1. **Parcourir les skills** : Voir `templates/`, `agenticos/`, `services/`.
2. **Lire la doc** : Chaque skill a un `SKILL.md` avec workflow, exemples, ré «fé««rences.
3. **Exé««cuter** : L'agent utilise le skill via son nom/triggers.

## Structure

```
skills-brain/
├── README.md                 # Ce fichier
├── SPECIFICATION.md          # Vision, objectifs, roadmap, standards
├── templates/                # Skills gén ériques
│   ├── README.md
│   ├── template-deployment/
│   ├── template-security-audit/
│   ├── template-migration/
│   └── template-eval/
├── agenticos/                # Skills AgenticOS
│   └── ... (à«« venir)
└── services/                 # Skills externes
    └── ... (à«« venir)
```

## Skills Disponibles

### Templates (Gé««né««riques)

| Skill | Description | Triggers |
|-------|-------------|----------|
| [`template-deployment`](./templates/template-deployment/SKILL.md) | Dé «ployer/rollback un service | `deploy`, `rollback` |
| [`template-security-audit`](./templates/template-security-audit/SKILL.md) | Audit sé «curité«« | `security audit` |
| [`template-migration`](./templates/template-migration/SKILL.md) | Migrations DB | `run migration` |
| [`template-eval`](./templates/template-eval/SKILL.md) | É «valuation qualité «| `evaluate` |

### AgenticOS (À«€ Venir)

- `agenticos-deploy`
- `agenticos-security-scan`
- `agenticos-migration-runner`
- `agenticos-agent-audit`

### Services Externes (À«€ Venir)

- `zabbix-proxi-monitor`
- ...

## Standards de Qualité

- **Frontmatter YAML** : name, description, triggers, license, version
- **Workflow** : É «tapes numé««roté««es, reproductibles
- **Tests** : Happy path + edge cases
- **Versioning** : Sé «mantique (MAJOR.MINOR.PATCH)

## Contribution

1. Fork le dé «pô«««.
2. Cr é er une branche (`feature/mon-skill`).
3. Suivre le template dans `templates/`.
4. Ajouter tests + documentation.
5. Ouvrir une Pull Request.

Voir [`SPECIFICATION.md`](./SPECIFICATION.md) pour dé «tails.

## License

MIT — Voir [`LICENSE`](./LICENSE).

## Contact

- **Author** : S R
- **Email** : 122878753+sramiweb@users.noreply.github.com
- **Repo** : https://github.com/sramiweb/skills-brain
