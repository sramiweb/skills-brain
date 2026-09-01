# Changelog

Tous les changements notables sont documenté««s ici.

Format bas é sur [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- 4 templates gén ériques (`template-deployment`, `template-security-audit`, `template-migration`, `template-eval`)
- 4 skills AgenticOS (`agenticos-deploy`, `agenticos-security-scan`, `agenticos-migration-runner`, `agenticos-agent-audit`)
- 1 skill externe (`zabbix-proxi-monitor`)
- `SPECIFICATION.md` (vision, objectifs, roadmap, standards)
- `README.md` principal + `templates/README.md` + `agenticos/README.md` + `services/README.md`
- `LICENSE` (MIT)
- CI/CD : `.github/workflows/validate-skills.yml`
- Scripts : `scripts/validate-skills.sh`

### Todo (Phase 2)
- 4-9 autres skills externes (Grafana, Prometheus, Vault, K8s, etc.)
- Tests automatisé««s pour chaque skill
- Documentation des APIs externes

## [1.0.0] - 2026-09-01

### Added
- Initial release
- Structure de base (`templates/`, `agenticos/`, `services/`)
- Documentation complète
