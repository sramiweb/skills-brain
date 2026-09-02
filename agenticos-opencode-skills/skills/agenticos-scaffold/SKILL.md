---
name: agenticos-scaffold
description: Scaffolder et étendre une infra agentique AgenticOS/Hermes — structure de dépôt, agents.yaml, routing-policies.yaml, orchestrateur, scheduler enqueue-only, workers sandboxés. À utiliser pour créer, initialiser ou faire évoluer une infra AgenticOS : nouvel agent, nouveau tenant, politique de routage, outil MCP. Mots-clés : scaffold, init, bootstrap, agents.yaml, routing policies.
---

# AgenticOS Scaffold

Construire une infra AgenticOS dont le **déclaré dit la vérité** : chaque ligne de YAML correspond à un comportement réellement implémenté, branché et testé. Le travers n°1 à éviter est le YAML qui ment (politique déclarée jamais chargée, `force_local` non enforcé, `human_validation` contournable).

## Invariants à respecter dans tout scaffold

1. **Un seul chemin d'exécution** : scheduler (enqueue-only) → orchestrateur → worker sandboxé. Jamais de `run.py` lancé directement sur l'hôte, jamais de shadow cron exécutant du code agent.
2. **Sémantique centralisée** : quotas, validation humaine, `force_local`, sandbox, livraison vivent à **un seul endroit** du code (l'orchestrateur), pas dupliqués par agent.
3. **Fail-closed partout** : rôle par défaut = refus, réseau = deny-all, outil non déclaré = interdit.
4. **Chaque politique a son test négatif** : toute règle de `routing-policies.yaml` est livrée avec un test prouvant qu'elle bloque réellement.
5. **Observabilité non désactivable** : traces LLM systématiques dès le premier agent.

## Déroulé

1. **Cadrer** : identifier ce qu'on scaffold (infra complète, nouvel agent, nouveau tenant, nouvelle politique). Demander ce qui manque : classes de données (S0/S1), canaux de livraison, modèles disponibles derrière la passerelle.
2. **Poser la structure** : suivre `references/structure-projet.md` — arborescence du dépôt, placement de chaque composant, conventions de nommage.
3. **Déclarer les agents** : partir de `assets/templates/agents.yaml` — chaque agent porte `data_class`, `force_local` si S1, `human_validation: required` si action externe, quotas explicites.
4. **Déclarer le routage** : partir de `assets/templates/routing-policies.yaml` — les 3 politiques minimales (`block-secrets`, `s1-local-only`, `external-action-validation`) sont non optionnelles.
5. **Implémenter avant de déclarer plus** : ne jamais écrire une clé YAML dont l'enforcement n'existe pas encore. Ordre d'implémentation : orchestrateur + dispatch → enforcement des politiques → scheduler → livraison avec `check_output`.
6. **Livrer les preuves** : chaque brique se termine par une preuve exécutable (test négatif, trace, commande de vérification), pas par « vérifier que… ».

## Profils d'agents de référence

Toujours couvrir ces 3 profils dans un scaffold complet (ils exercent tous les maillons) :

- **Agent planifié simple** (ex. `sre-health`) : S0, lecture seule, `human_validation: never`.
- **Agent à données sensibles S1** (ex. `syndic-rapporteur`) : `force_local: true`, cloisonné par `tenant_id`, validation avant livraison.
- **Agent à action externe** (ex. `outreach-operator`) : `human_validation: required`, approbation liée au **hash de l'action** (non contournable par reformulation).

## Règles de conduite

- Refuser de scaffolder un contournement : pas de `--auto-approve` en prod, pas de chemin hors sandbox, pas de secret en clair « temporaire ».
- En cas d'ambiguïté ou de conflit d'exigences, le remonter à l'utilisateur — ne jamais trancher silencieusement.
- Après tout scaffold, proposer de vérifier le résultat avec le skill `agenticos-audit`.
