# Auto-apprentissage et méta-agents — AgenticOS

Le maillon 9 de la boucle d'autonomie : le système apprend de ses propres exécutions, **sans jamais se modifier sans veto humain**.

## Architecture de référence

1. **Observation** : les méta-agents lisent traces, échecs (`error_detail`), coûts, latences — accès **read-only** par défaut.
2. **Proposition** : toute amélioration devient une ligne `meta_proposals` (state machine : `proposed → approved|rejected|vetoed → applied → verified`), traçable et horodatée.
3. **Validation humaine obligatoire** : aucune mutation (config, prompt, code, routing) sans approbation humaine. Pas d'`--auto-approve` sur ce chemin.
4. **Veto security-sentinel** : un méta-agent dédié peut passer toute proposition à `vetoed` (ex. proposition affaiblissant une politique de sécurité).
5. **Vérification post-changement** : après application, vérifier que le déclaré = l'exécuté (diff YAML ↔ runtime, test négatif rejoué).

## Règles strictes

- Écriture uniquement dans les tables `meta_*` ; jamais d'écriture directe dans les tables métier ou mémoire.
- Jamais de code métier dans le socle : les agents générés par les méta-agents sont écrits dans le package métier.
- Suite de tests verte avec le package métier absent (non-régression du socle).
- Une proposition non vérifiée après application reste ouverte et remonte en alerte.

## Honnêteté d'état

Toujours distinguer et annoncer explicitement, pour chaque méta-agent :

- **Spécifié** : décrit dans un doc/YAML, rien ne s'exécute.
- **Codé** : le code existe, pas encore branché sur le runtime.
- **Opérationnel** : exécuté, observé en environnement de qualification, avec preuve.

Ne jamais présenter un méta-agent spécifié ou codé comme opérationnel — c'est l'écart déclaré/exécuté classique détecté par l'audit.

## Preuves de fin

- Proposition créée → visible dans `meta_proposals` avec état `proposed`.
- Mutation tentée sans approbation → refusée et journalisée.
- Proposition approuvée puis appliquée → vérification automatique déclaré = exécuté, passage à `verified`.
- Veto du security-sentinel → proposition bloquée, motif enregistré.
