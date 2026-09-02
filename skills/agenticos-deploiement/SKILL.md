---
name: agenticos-deploiement
description: Déployer et opérer le socle d'une infra AgenticOS/Hermes — passerelle LLM unique (LiteLLM) avec fallbacks et budgets, scheduler fiable, reaper d'exécutions zombies, observabilité Langfuse non désactivable, socle K8s/Terraform (principes P1–P8, Kustomize, Argo CD). À utiliser pour déployer, migrer, opérer ou dépanner l'infra : passerelle, scheduler/cron, monitoring, dashboards, runbook.
---

# AgenticOS Déploiement & Opérations

Déployer un socle où le déclaré = l'exécuté, observable par construction, et où **un seul chemin d'exécution** existe (scheduler enqueue-only → orchestrateur → worker sandboxé).

## Déroulé

1. **Passerelle LLM d'abord** : suivre `references/passerelle-llm.md` — passerelle unique, ≥ 2 réplicas, fallbacks cohérents, budgets par tenant avec alerte à 80 %. Aucun composant ne contacte un fournisseur directement.
2. **Scheduler fiable** : matcher DOW testé (décalage jour de semaine = bug classique), fuseaux horaires explicites, enqueue-only, ne crashe jamais sur un service externe down (log + retry).
3. **Fiabilité des exécutions** : reaper au démarrage (`running > timeout → failed`), `error_detail = (stderr or stdout)[-2000:]`, idempotence des relances, taux d'échecs diagnosables > 90 %.
4. **Observabilité non désactivable** : traces Langfuse systématiques (aucune option pour les couper), dashboards (échecs/agent, coût/tenant, occupation mémoire, files, latence passerelle, saturation workers).
5. **Socle K8s/Terraform si applicable** : suivre `references/socle-k8s.md` — principes P1–P8 non négociables, overlays/tfvars pour toute valeur client, backend d'état isolé par client, ADR pour tout écart de stack.
6. **Vérification post-déploiement** : le déclaré correspond à l'exécuté (diff config ↔ runtime, un appel de démo produit une trace visible). Proposer ensuite un passage du skill `agenticos-audit`.

## Règles de conduite

- Jamais de big bang : migrations item par item avec double-run de validation ; backup + test de restauration avant toute migration de données.
- Tests existants verts après chaque phase + tests des nouvelles preuves de fin ; journal de refonte (`refonte-log.md`) tenu à jour.
- Un tiers doit pouvoir reproduire le déploiement en suivant uniquement le README/runbook.
- Tout changement de chaîne de fallback exige un graph coût/latence avant-après.
- En cas d'échec : diagnostiquer et proposer 2 options — pas de contournement silencieux.
