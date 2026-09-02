---
name: agenticos-memoire
description: Concevoir la mémoire et l'auto-apprentissage d'une infra AgenticOS/Hermes — état inter-runs (agent_state), mémoire vectorielle cloisonnée par tenant (Qdrant), rétention et consolidation, tables meta_* avec validation humaine des propositions de méta-agents. À utiliser pour ajouter persistance entre runs, recherche par tenant, politique de rétention, ou méta-agent d'amélioration. Mots-clés : mémoire, tenant_id, rétention, auto-apprentissage, meta_proposals.
---

# AgenticOS Mémoire & Auto-apprentissage

La mémoire est le maillon 6 de la boucle d'autonomie : sans elle, aucun agent n'est réellement autonome. Deux exigences non négociables : **cloisonnement par tenant** (`tenant_id` NOT NULL partout) et **rétention active** (sinon saturation en ~3 mois).

## Déroulé

1. **État inter-runs** : implémenter `agent_state` selon `assets/schema.sql` — un run N+1 doit pouvoir relire l'état du run N. Preuve : test relançant un agent et vérifiant la relecture.
2. **Mémoire vectorielle** : suivre `references/schema-et-retention.md` — répartition par tenant vérifiable, recherche filtrée par tenant retournant les bons résultats (test cross-tenant → 0 ligne).
3. **Rétention** : consolidation/résumé des sessions > 30 j, archivage, cron de consolidation actif, alerte d'occupation à 80 % (95 % = saturation imminente). Sans rétention, ne pas livrer.
4. **Backup avant toute migration** de données, avec test de restauration réel — jamais de big bang, migration item par item avec double-run de validation.
5. **Auto-apprentissage (méta-agents)** : suivre `references/auto-apprentissage.md` — read-only par défaut, écriture uniquement dans `meta_*`, validation humaine obligatoire avant toute mutation, veto du security-sentinel, vérification post-changement (déclaré = exécuté).

## Pièges connus à éviter

- `tenant_id` NULL accepté quelque part → fuite inter-tenant garantie.
- Occupation mémoire > 80 % sans politique de rétention → saturation.
- Auto-modification sans veto humain → le méta-agent devient un chemin d'exécution non contrôlé.
- Confondre spécifié / codé / opérationnel pour un méta-agent : toujours dire lequel des trois est livré.

## Règles de conduite

- Toute migration de schéma : backup + test de restauration d'abord, ensuite migration avec rollback documenté dans le runbook.
- Chaque brique mémoire se livre avec sa preuve exécutable (relecture d'état, filtre tenant, alerte 80 % déclenchée en test).
- Après implémentation, proposer une vérification avec le skill `agenticos-audit` (maillon 6 et maillon 9).
