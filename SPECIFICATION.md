# Skills-Brain — Spé««ifications du Projet

## Vision

**Skills-Brain** est un dépôt centralisé«« de skills (compé««tences) réutilisables pour agents AI (OpenCode, Claude Code, etc.). Chaque skill est un workflow autonome, testé«« et documenté««, décrivait une tâche spécifique que l'agent peut exé««cuter.

## Objectif Principal

Fournir une bibliothèque de skills **fiable, maintenable et extensible** pour :
- **Accé««lé««rer le développement** : Les agents réutilisent des workflows éprouvé««s au lieu de réinventer chaque tâche.
- **Garantir la qualité** : Chaque skill inclut tests, exemples et critères de validation.
- **Faciliter la maintenance** : Structure standardisé««e, documentation claire, versioning s émantique.

## Périmè««tre

### Inclus
- Skills gén ériques (templates) pour workflows communs (dé««ploiement, audit sécurité, migration, évaluation).
- Skills spé «cifiques à AgenticOS (implé««mentations réelles des templates).
- Skills pour services externes (Zabbix, Proxi, etc.).
- Documentation, tests, exemples d'usage.

### Exclus
- Code d'application métier (ce n'est pas un dépôt de microservices).
- Configuration d'infrastructure (Terraform, Ansible, etc.).
- Secrets ou credentials (utiliser des variables d'environnement ou vaults externes).

## Architecture

```
skills-brain/
├── SPECIFICATION.md          # Ce fichier
├── README.md                 # Vue d'ensemble du projet
├── templates/                # Skills gén ériques réutilisables
│   ├── README.md
│   ├── template-deployment/
│   ├── template-security-audit/
│   ├── template-migration/
│   └── template-eval/
├── agenticos/                # Skills spé «cifiques à AgenticOS
│   ├── agenticos-deploy/
│   ├── agenticos-security-scan/
│   ├── agenticos-migration-runner/
│   └── agenticos-agent-audit/
└── services/                 # Skills pour services externes
    ├── zabbix-proxi-monitor/
    └── .../
```

## Standards de Qualité

### Structure d'un Skill

Chaque skill (`SKILL.md`) doit contenir :
1. **Frontmatter YAML** : name, description, triggers, license, compatibility, metadata (author, version, category).
2. **Purpose** : Description claire de l'objectif.
3. **Workflow** : É tapes numé««roté««es, reproductibles.
4. **Examples** : Au moins un "happy path" avec Input/Expected/Actual/Status.
5. **References** : Liens vers skills liés ou documentation externe.

### Versioning

- **Sé««mantique** : `MAJOR.MINOR.PATCH` (ex: `1.0.0`).
- **MAJOR** : Changements incompatibles (workflow modifié««).
- **MINOR** : Nouvelles fonctionnalit é s (workflow étendu, rétrocompatible).
- **PATCH** : Corrections de bugs, documentation.

### Tests

- Chaque skill doit avoir des **tests automatisé««s** (si applicable).
- Les tests doivent couvrir :
  - **Happy path** : Cas nominal.
  - **Edge cases** : Cas limites (entr é es invalides, échecs réseau, etc.).
  - **Error handling** : Gestion des erreurs explicite.

### Documentation

- **README.md** à la racine : Vue d'ensemble, installation, usage, contribution.
- **README.md** par catégorie (`templates/`, `agenticos/`, `services/`) : Liste des skills, liens.
- **SKILL.md** : Documentation détaillé««e de chaque skill.

## Roadmap

### Phase 1 — Fondations (Q4 2026)
- [x] Créer les 4 templates gén ériques (deployment, security-audit, migration, eval).
- [ ] Créer les 4 skills AgenticOS correspondants.
- [ ] Ajouter tests et exemples pour chaque skill.
- [ ] Documentation complète (README, contribution, changelog).

### Phase 2 — Expansion (Q1 2027)
- [ ] Ajouter 5-10 skills pour services externes (Zabbix, Proxi, etc.).
- [ ] Inté««gration CI/CD (validation automatique des skills).
- [ ] Outils de validation (linting, tests automatisé««s).

### Phase 3 — Maturité«« (Q2 2027)
- [ ] 50+ skills disponibles.
- [ ] Communauté«« de contributeurs.
- [ ] Inté««gration avec plateformes AI (marketplace, registry).

## Critè««res de Succè««s

- **Adoption** : 10+ projets utilisant skills-brain.
- **Qualité««** : 95%+ de tests passants, 0 critical bugs.
- **Maintenance** : Temps moyen de résolution de bug < 48h.
- **Documentation** : 100% des skills documenté««s avec exemples.

## Contribution

1. Fork le dé «pô«««.
2. Cr é er une branche (`feature/mon-skill`).
3. Ajouter le skill (suivre le template).
4. Ajouter tests et documentation.
5. Ouvrir une Pull Request.

## License

MIT — Voir `LICENSE`.

## Contact

- **Author** : S R
- **Email** : 122878753+sramiweb@users.noreply.github.com
- **Repo** : https://github.com/sramiweb/skills-brain
