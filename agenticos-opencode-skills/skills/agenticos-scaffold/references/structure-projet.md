# Structure de dépôt AgenticOS — référence

## Sommaire
1. Arborescence cible
2. Rôle de chaque composant
3. Conventions

## 1. Arborescence cible

```
agenticos-infra/
├── config/
│   ├── agents.yaml              # déclaration des agents (source de vérité)
│   ├── routing-policies.yaml    # politiques appliquées AVANT dispatch
│   └── values-communs.yaml      # si socle K8s : commun / modules_optionnels / personnalisable
├── orchestrateur/
│   ├── dispatch.py              # enforcement des politiques, quotas, force_local
│   ├── approval.py              # validation humaine liée au hash de l'action
│   ├── deliver.py               # livraison + check_output sur tous les canaux
│   └── audit.py                 # journal : qui, quoi, quand, coût (jamais de secret)
├── scheduler/
│   └── scheduler.py             # enqueue-only : aucune logique métier, aucun appel LLM
├── workers/
│   └── runner.py                # exécution sandboxée (gVisor/Kata/conteneur isolé)
├── memoire/
│   ├── schema.sql               # agent_state, memoire vectorielle, meta_*
│   └── retention.py             # consolidation, résumé > 30 j, archivage
├── gateway/
│   └── litellm.config.yaml      # passerelle LLM unique, fallbacks, budgets
├── ops/
│   ├── reaper.py                # zombies : running > timeout → failed
│   ├── dashboards/              # échecs/agent, coût/tenant, occupation mémoire
│   └── runbook.md               # redémarrage, restauration, journal des migrations
├── tests/
│   ├── test_policies_negative.py  # chaque politique bloque réellement
│   └── test_loop_e2e.py           # une exécution de bout en bout par profil
└── docs/
    └── ADR-*.md                 # tout écart à la stack justifié
```

## 2. Rôle de chaque composant

| Composant | Responsabilité unique | Ne doit jamais |
|---|---|---|
| `scheduler` | Enfiler les exécutions dues (matcher DOW correct, fuseaux horaires) | Exécuter du code agent, appeler un LLM, crasher sur un service down |
| `orchestrateur` | Charger routing-policies **avant dispatch**, quotas, validation, audit | Contacter un fournisseur LLM directement (passerelle uniquement) |
| `workers` | Exécuter l'agent en sandbox, capturer `error_detail = (stderr or stdout)[-2000:]` | Tourner hors sandbox, hériter d'env pointant hors passerelle |
| `memoire` | État inter-runs, recherche filtrée par tenant | Accepter un `tenant_id` NULL |
| `gateway` | Point unique d'accès LLM, fallbacks, budgets par tenant | Être contournée par un composant |
| `ops/reaper` | Marquer `failed` les exécutions `running > timeout` au démarrage | Supprimer des exécutions sans trace d'audit |

## 3. Conventions

- **Classes de données** : `S0` (non sensible) / `S1` (sensible, type Loi 18.00 / RGPD). S1 ⇒ `force_local: true` + cloisonnement `tenant_id` NOT NULL partout.
- **Modèles** : alias de passerelle (`fast`, `strong`, `local`), jamais de nom de fournisseur dans `agents.yaml`.
- **Nommage agents** : verbe-domaine (`sre-health`, `syndic-rapporteur`, `outreach-operator`).
- **Idempotence** : relancer un agent deux fois ne produit ni doublon ni double application — clé d'idempotence par (tenant, agent, fenêtre de schedule).
- **Preuve de fin** : chaque brique livrée avec un critère exécutable (test, commande, trace attendue).
