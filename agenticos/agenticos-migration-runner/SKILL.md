---
name: agenticos-migration-runner
description: Use this skill when the user wants to run database migrations on AgenticOS. Triggers on "run migration agenticos", "migrate agenticos", "agenticos migration". Implements template-migration.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: agenticos
  template: template-migration
---

# Skill: AgenticOS Migration Runner

## Purpose

Exé««cute des migrations de base de donné «es sur AgenticOS avec backup, validation, et rollback automatique en cas d'é««chec.

## Workflow

1. **Valider migrations** : Vérifier que les fichiers de migration existent et sont valides.
2. **Backup** : Snapshot de la DB avant migration (dump SQL + backup complet).
3. **Run migration** : Exé««cuter les migrations (up) dans l'ordre.
4. **Vé««rifier** : Tester l'inté««grité«« des donné «es, checksums.
5. **Documenter** : MAJ CHANGELOG, version DB, logs.

## Examples

### Happy path
- **Input** : "Run migration on `api-service` DB (agenticos)"
- **Expected** : Backup OK, migrate OK, verify OK
- **Actual** : 5 migrations appliqu ées en 2m 10s
- **Status** : PASS · Level: L1

### É «chec (rollback)
- **Input** : "Run migration on `payment-service` DB (agenticos)"
- **Expected** : É «chec, rollback automatique
- **Actual** : Migration 3/5 é «chou ée, rollback OK
- **Status** : FAIL · Level: L1

## References

- Template : [`template-migration`](../../templates/template-migration/SKILL.md)
- Doc AgenticOS : https://docs.agenticos.io/migrations
