---
name: agenticos-migration
description: Migrer un composant d'une infra AgenticOS/Hermes vers une nouvelle cible sans big bang — sortir l'exécution métier d'Hermes Agent, remplacer un scheduler, changer de passerelle ou de store mémoire, montée de version du socle. Méthode : inventaire des chemins d'exécution, pattern strangler, double-run de validation, bascule item par item avec preuves de fin et rollback. À utiliser dès qu'on déplace, remplace ou décommissionne un composant d'exécution, de mémoire ou de routage. Mots-clés : migration, strangler, double-run, bascule, décommissionnement, sortir de Hermes.
---

# AgenticOS Migration

Règle d'or : **jamais de big bang**. Toute migration se fait item par item, avec double-run de validation et preuve de fin exécutable à chaque étape. Une migration « en une fois » est le chemin le plus court vers les exécutions perdues, les doublons et les données corrompues.

## Déroulé

1. **Inventaire avant tout** : cartographier les chemins d'exécution réels (scheduler hôte ∥ orchestrateur ∥ shadow crons ∥ cron Hermes), les données concernées et leurs tenants. Suivre `references/plan-type.md`. Une migration qui démarre sans inventaire complet recrée des chemins parallèles.
2. **Backup + test de restauration réel** avant de toucher à la moindre donnée.
3. **Strangler, pas remplacement** : la nouvelle cible est construite à côté de l'ancienne ; le trafic bascule composant par composant, jamais globalement.
4. **Double-run** : ancien et nouveau chemin tournent en parallèle sur le même périmètre ; comparer les sorties. Seul le double-run prouve que déclaré = exécuté sur le nouveau chemin.
5. **Bascule item par item** : un agent / un tenant / un cron à la fois, chacun avec sa preuve de fin et son rollback documenté. En cas d'échec : diagnostiquer, proposer 2 options — pas de contournement silencieux.
6. **Décommissionnement** : l'ancien chemin n'est retiré qu'après une période d'observation complète (cycle entier des schedules), et son retrait est lui-même audité (0 résidu : crons, env, secrets, DNS).
7. **Journal** : tenir `refonte-log.md` et le runbook à jour après chaque étape ; tests existants verts en permanence.

## Cas d'usage typiques

- **Sortir l'exécution métier d'Hermes Agent** vers l'orchestrateur AgenticOS : migrer les crons métier un par un, Hermes relégué au rôle opérateur (voir `agenticos-hermes-integration`).
- **Remplacer le scheduler** (cron hôte → orchestrateur enqueue-only) : migrer les crons un par un avec double-run, jamais tous ensemble.
- **Changer de store mémoire** ou migrer le schéma : voir `agenticos-memoire` (backup, double-run, journal).
- **Montée de version du socle K8s/Terraform** : respecter P8 (rétro-compatibilité), overlay par overlay.

## Règles de conduite

- Une étape sans preuve de fin exécutable n'est pas terminée — « vérifier que… » n'est pas une preuve.
- Les données S1 migrent avec cloisonnement vérifié à chaque étape (`tenant_id` NOT NULL, 0 fuite cross-tenant démontrée).
- Après la migration, passer le skill `agenticos-audit` sur le périmètre migré (maillons 2, 6 et 8 en priorité).
