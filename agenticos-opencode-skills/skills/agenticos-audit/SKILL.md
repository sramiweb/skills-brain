---
name: agenticos-audit
description: Auditer une infrastructure agentique AgenticOS/Hermes — autonomie réelle des agents (boucle des 9 maillons : déclaration → planification → décision → appel outils → observation → mémoire → coordination → reprise → amélioration), sécurité, robustesse, mémoire, skills, auto-apprentissage, conformité socle. À utiliser pour tout audit, revue, analyse de risques ou diagnostic d'autonomie d'une infra AgenticOS, que l'entrée soit un dépôt, des YAML (agents.yaml, routing-policies), des logs, des crontabs ou une description verbale.
---

# AgenticOS Audit

Auditer une infrastructure AgenticOS/Hermes de manière structurée, honnête et actionnable. L'objet central est l'**autonomie réelle et démontrée** des agents — jamais la seule présence de fichiers de configuration.

## Règles de conduite de l'audit

1. **Ne jamais inventer** : tout constat pointe vers une preuve (fichier, ligne, log, trace, commande). Information manquante → section « Informations manquantes », jamais de supposition.
2. **Démontré en exécution ou rien** : un contrôle n'est « présent » que s'il est implémenté, branché, testé et observé en environnement de qualification. Déclaré ≠ fonctionnel.
3. **Vérifier l'écart déclaré vs exécuté** : travers n°1 d'AgenticOS = YAML qui ment (politiques jamais chargées, `force_local` non enforcé, `human_validation` contournée par `--auto-approve`).
4. **Chercher les chemins d'exécution multiples** : scheduler hôte ∥ orchestrateur ∥ shadow crons. Toute voie contournant sandbox/quotas/validation = risque majeur.
5. **Prioriser par exploitabilité réelle** : un secret en clair lu par un agent > une bonne pratique manquante.
6. **Chaque finding = constat → preuve → risque → criticité → recommandation → effort estimé.**

## Déroulé

1. **Cadrage** : identifier l'entrée (dépôt, configs, logs, crontabs, description). Entrée verbale uniquement → auditer sur déclaration en le disant explicitement.
2. **Cartographie** : composants et chemins d'exécution (orchestrateur, scheduler, crons shadow, passerelle, mémoire, agents, connecteurs MCP, console, méta-agents).
3. **Audit de la boucle d'autonomie (cœur)** : charger `references/boucle-autonomie.md` et noter les **9 maillons** (déclaration → planification → décision → appel outils → observation → mémoire → coordination → reprise → amélioration) pour un échantillon d'au moins 3 agents représentatifs, dont un agent S1 et un agent à action externe. Suivre au moins une exécution de bout en bout.
4. **Audit transverse par axes** : charger les checklists pertinentes de `references/` :
   - `references/checklist-securite.md` — secrets, rôles/fail-open, données S1/S0, sandbox, réseau, guardrails, audit trail.
   - `references/checklist-architecture.md` — chemins d'exécution, passerelle LLM, fallback/routing, mémoire et rétention, idempotence, erreurs, tests.
   - `references/checklist-conformite.md` — principes P1–P8 et traçabilité EF/ENF (uniquement si socle K8s/Terraform).
5. **Scoring et synthèse** : appliquer `references/grille-scoring.md` (P0/P1/P2, quick wins vs chantiers). La boucle d'autonomie est notée par agent : une chaîne vaut son maillon le plus faible.
6. **Rapport** : produire le rapport selon `references/format-rapport.md` — synthèse priorisée en tête, grille des 9 maillons par agent audité, findings détaillés, plan ordonné (Jour 0 d'abord).

## Points chauds connus d'AgenticOS (toujours vérifier)

- **Jour 0** : rôle par défaut fail-open (`AOS_DEFAULT_ROLE`), secrets dans l'audit log (`aos_audit`), mots de passe faibles sur consoles, bugs de scheduling (matcher DOW), code sans remote git.
- **Honnêteté** : `routing-policies.yaml` chargé ? `block-secrets` / `s1-local-only` appliqués avant dispatch ? `human_validation: required` réellement bloquante ?
- **Fallback LLM** : chaîne cohérente (un modèle `fast` fallback de tout = risque coût/dérive) ; monitoring coût/latence avant-après tout changement.
- **Mémoire** : `tenant_id` NOT NULL partout, occupation (alerte 80 %), politique de rétention, sauvegarde avant toute migration.
- **Exécutions** : reaper zombies (`running > timeout → failed`), `error_detail` capturant stderr, taux d'échecs diagnosable > 90 %.
- **Auto-apprentissage** : propositions traçables, validation humaine obligatoire avant toute mutation, vérification post-changement déclaré = exécuté ; distinguer spécifié / codé / opérationnel pour les méta-agents.

## Style

- Français, direct, sans flatterie. Dire clairement ce qui est cassé.
- Pas de contournement silencieux : ambiguïté ou conflit d'exigences → remonté dans le rapport, jamais tranché à la place de l'utilisateur.
- Le rapport se termine toujours par un plan ordonné : sécurité immédiate (J0) → honnêteté du système → unification → mémoire → gouvernance.
