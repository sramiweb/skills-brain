# Schéma mémoire et rétention — AgenticOS

## Sommaire
1. État inter-runs (`agent_state`)
2. Mémoire vectorielle (Qdrant)
3. Politique de rétention
4. Monitoring d'occupation
5. Migrations

## 1. État inter-runs

Table de référence : `agent_state (tenant_id, agent, key, value JSONB, updated_at)` — voir `assets/schema.sql`.

- `tenant_id` : NOT NULL, clé primaire composite avec `agent` et `key`. Aucune ligne orpheline de tenant.
- Lecture au démarrage du run : l'agent recharge ses clés avant de planifier.
- Écriture en fin de run : état minimal suffisant pour reprendre (dernière position, curseurs, compteurs).
- **Preuve de fin** : run N écrit une clé → run N+1 la relit et agit différemment (test automatisé).

## 2. Mémoire vectorielle

- Une collection par tenant OU une collection partagée avec filtre `tenant_id` obligatoire — dans les deux cas, la répartition par tenant est **vérifiable** (comptage par tenant).
- Toute recherche passe par une couche qui injecte le filtre tenant — jamais de recherche brute exposée aux agents.
- **Preuve de fin** : insérer des souvenirs de deux tenants, rechercher en tant que tenant A → 0 résultat du tenant B.

## 3. Politique de rétention

Sans rétention active, la mémoire sature en ~3 mois. Implémenter dès le départ :

| Âge | Action |
|---|---|
| < 30 j | Mémoire chaude, inchangée |
| > 30 j | Résumé de session (consolidation par agent), détails archivés |
| > rétention tenant | Purge ou archivage objet, selon la classe de données (S1 : règles légales du tenant) |

- Cron de consolidation **actif** et surveillé (échec → alerte, pas silence).
- Consolidation idempotente : relancer deux fois ne duplique pas les résumés.
- **Preuve de fin** : jeu de données vieilli artificiellement → consolidation produit les résumés attendus, une seule fois.

## 4. Monitoring d'occupation

- Seuils : alerte à **80 %**, 95 % = saturation imminente (action immédiate).
- Dashboard : occupation par tenant, croissance hebdomadaire, top agents consommateurs.
- Budgets mémoire par tenant cohérents avec les budgets tokens de la passerelle.

## 5. Migrations

1. Backup complet + **test de restauration réel** avant toute migration.
2. Migration item par item avec double-run de validation (ancien ∥ nouveau, comparaison).
3. Journal des migrations dans `ops/runbook.md` : date, contenu, rollback.
4. En cas d'échec : diagnostiquer, proposer 2 options — jamais de contournement silencieux.
