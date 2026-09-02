# Plan type d'une migration AgenticOS

## Sommaire
1. Phase 0 — Inventaire et gel
2. Phase 1 — Construction de la cible (strangler)
3. Phase 2 — Double-run
4. Phase 3 — Bascule item par item
5. Phase 4 — Décommissionnement
6. Modèles de preuves de fin

## Phase 0 — Inventaire et gel

- [ ] Tous les chemins d'exécution recensés : `crontab -l`, systemd timers, scheduler AgenticOS, crons Hermes, lancements manuels documentés. **Preuve** : tableau chemins × agents, validé par l'équipe.
- [ ] Données concernées inventoriées par tenant et par classe (S0/S1). **Preuve** : liste des tables/collections avec volumétrie.
- [ ] Backup complet + **test de restauration réel** (restaurer sur un environnement jetable et requêter). **Preuve** : restauration rejouée, pas seulement archive présente.
- [ ] Gel des changements sur le périmètre migré pendant la migration.

## Phase 1 — Construction de la cible (strangler)

- [ ] La cible tourne en qualification, branchée sur la passerelle, le sandbox et l'audit — les mêmes invariants que le reste du socle. **Preuve** : un agent de démo s'exécute sur la cible avec trace Langfuse et ligne d'audit.
- [ ] Les politiques de routage s'appliquent sur la cible **avant dispatch**. **Preuve** : tests négatifs rejoués sur la cible (block-secrets, s1-local-only, validation humaine).

## Phase 2 — Double-run

- [ ] Ancien et nouveau chemin actifs en parallèle sur un périmètre réduit (1 agent non critique, 1 tenant pilote). **Preuve** : N exécutions des deux côtés, sorties comparées automatiquement — écart = 0 ou expliqué.
- [ ] Pas de double effet de bord : un seul des deux chemins livre réellement (l'autre en mode shadow/dry-run). **Preuve** : aucune livraison en double observée.

## Phase 3 — Bascule item par item

Ordre : agents les moins critiques d'abord, S1 et actions externes en dernier.

- [ ] Pour chaque item : bascule + observation d'un cycle de schedule complet + rollback documenté. **Preuve par item** : exécutions réussies sur la cible sur un cycle entier, zéro sur l'ancien chemin.
- [ ] Métriques surveillées pendant la bascule : taux d'échec, coût, latence P95 (seuils de `agenticos-eval`). **Preuve** : pas de régression sur le périmètre basculé.
- [ ] En cas d'échec : rollback exécuté, diagnostic écrit, 2 options proposées. Jamais de contournement silencieux.

## Phase 4 — Décommissionnement

- [ ] Ancien chemin retiré après observation complète. **Preuve** : 0 résidu — crons supprimés (`crontab -l` vide de l'ancien), env/nettoyée, secrets révoqués, DNS/endpoints retirés.
- [ ] `refonte-log.md` et runbook mis à jour : architecture réelle après migration, journal des étapes. **Preuve** : un tiers reproduit l'état actuel en suivant le runbook.
- [ ] Audit post-migration du périmètre (maillons 2, 6, 8). **Preuve** : rapport d'audit sans P0/P1 résiduel.

## Modèles de preuves de fin

| Étape | Mauvaise preuve | Bonne preuve |
|---|---|---|
| Bascule d'un agent | « vérifier qu'il tourne » | 5 exécutions réussies sur la cible, 0 sur l'ancien chemin, trace Langfuse jointe |
| Migration mémoire | « les données sont migrées » | comptage par tenant identique des deux côtés + relecture run N+1 démontrée |
| Décommissionnement | « l'ancien est éteint » | `crontab -l`, services, secrets : inventaire à 0 résidu, rejoué par quelqu'un d'autre |
