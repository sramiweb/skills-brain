---
name: agenticos-deploy
description: Use this skill when the user wants to deploy/rollback a service on AgenticOS. Triggers on "deploy to agenticos", "agenticos deploy", "rollback agenticos". Implements template-deployment.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: agenticos
  template: template-deployment
---

# Skill: AgenticOS Deploy

## Purpose

Dé««ploie ou rollback un service sur la plateforme AgenticOS avec validation, backup, et health checks.

## Workflow

1. **Valider la cible** : Vérifier que le service existe dans le registry AgenticOS.
2. **Pre-deploy checks** :
   - Lancer les tests unitaires
   - Lancer le linting
   - Audit de sé «curité«« (dé««pendances, secrets)
3. **Backup** : Snapshot de la version actuelle (tag Git + backup DB si applicable).
4. **Dé««ployer** :
   - Build de l'image Docker
   - Push vers le registry
   - Mise à jour du deployment Kubernetes
5. **Health check** :
   - Vérifier les pods (ready/running)
   - Tester les endpoints critiques
   - Valider les métriques (latence, erreurs)
6. **Rapport** : Status (SUCCESS/FAILED) + logs + métriques.

## Examples

### Happy path
- **Input** : "Deploy `api-service` v2.1.0 to agenticos staging"
- **Expected** : Tests OK, backup OK, deploy OK, health OK
- **Actual** : Dé «ployé«« en 3m 20s, 0 erreurs
- **Status** : PASS · Level: L1

### Rollback
- **Input** : "Rollback `api-service` to v2.0.0 on agenticos"
- **Expected** : Restore backup, health OK
- **Actual** : Rollback OK en 1m 10s
- **Status** : PASS · Level: L1

### É «chec (tests)
- **Input** : "Deploy `api-service` v2.2.0 to agenticos"
- **Expected** : Tests échouent, deploy annulé««
- **Actual** : 3 tests échoué««s, rollback automatique
- **Status** : FAIL · Level: L1

## References

- Template : [`template-deployment`](../../templates/template-deployment/SKILL.md)
- Doc AgenticOS : https://docs.agenticos.io/deploy
