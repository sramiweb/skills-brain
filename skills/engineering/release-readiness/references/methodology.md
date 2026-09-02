# Methodologie — Release Readiness

## Objectif
Determiner si une release candidate peut etre publiee en production en toute securite.

## Entrees requises
- Liste des PR / commits inclus
- Resultats des tests (unit, integration, e2e)
- Tickets bloquants et leur statut
- Documentation de release / changelog
- Plan de rollback

## Checklist
1. **Code complete** : toutes les fonctionnalites attendues sont mergees.
2. **Tests passes** : taux de couverture stable, pas de regression.
3. **Quality gate** : lint, type check, audit CVE passes.
4. **Documentation** : changelog et release notes a jour.
5. **Ops ready** : migrations, variables d env, monitoring, rollback plan.
6. **Approbations** : code review et QA valides.
7. **Risque metier** : impact client acceptable.

## Sortie attendue
```yaml
verdict: GO | CONDITIONAL | NO-GO
confidence: HIGH | MEDIUM | LOW
blockers:
  - "..."
conditions:
  - "..."
actions:
  - priority: P0
    owner: "..."
    task: "..."
```

## Anti-patterns
- Ne pas donner de GO sans preuve.
- Ne pas ignorer un ticket bloquant ouvert.
- Ne pas declencher de deploiement automatique.
