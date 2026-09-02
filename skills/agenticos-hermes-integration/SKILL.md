---
name: agenticos-hermes-integration
description: Intégrer Hermes Agent (NousResearch) comme agent opérateur/personnel dans une infra AgenticOS sans compromettre le socle multi-tenant — routage LLM via la passerelle interne, durcissement (approval de commandes, quarantaine des skills du Hub), interdiction données S1 et credentials prod, isolation du workspace. À utiliser dès qu'on installe, configure ou durcit Hermes aux côtés d'AgenticOS, ou qu'Hermes touche à la messagerie, au scheduler ou à la mémoire. Mots-clés : Hermes, hermes-agent, agent opérateur, skills hub, gateway Telegram.
---

# AgenticOS — Intégration Hermes Agent

Hermes Agent est un **agent personnel auto-améliorant mono-utilisateur**. Rôle autorisé dans AgenticOS : assistant opérateur de l'équipe. Rôle interdit : exécuter des agents clients en production — l'exécution métier reste dans l'orchestrateur AgenticOS (tenants, quotas, guardrails, audit).

## Règles de coexistence (non négociables)

1. **Hermes ne touche jamais aux données S1** : aucune donnée client/tenant dans `MEMORY.md`, `USER.md`, la base SQLite locale ou les sessions. La mémoire Hermes est locale et mono-utilisateur — y mettre du S1 = fuite inter-tenant par construction.
2. **Tout le trafic LLM passe par la passerelle interne** : configurer Hermes sur l'endpoint OpenAI-compatible de la passerelle AgenticOS (LiteLLM), jamais de clé fournisseur directe (principe P2).
3. **Aucun credential de production dans Hermes** : pas de clés DB prod, pas de tokens d'admin dans sa config. Secrets via variables d'environnement injectées depuis le coffre, scope opérateur uniquement.
4. **Hermes n'exécute pas d'agents métier** : pas de cron Hermes lançant du code client (shadow cron = P0 d'audit). Son scheduler ne sert qu'à des tâches opérateur (rappels, rapports internes).
5. **Traçabilité** : les actions d'Hermes touchant l'infra passent par les mêmes canaux audités que tout opérateur humain.

## Durcissement à l'installation

Suivre `references/durcissement-hermes.md` — chaque mesure avec sa preuve :

- **Approval des commandes** activé (pas d'exécution shell silencieuse).
- **DM pairing** et liste d'utilisateurs autorisés sur la gateway messagerie.
- **Skills** : faire confiance uniquement aux skills projet revues ; tout skill du Skills Hub passe en **quarantaine** (revue de code avant activation) — un skill tiers peut exfiltrer ou exécuter arbitrairement.
- **Backend d'exécution isolé** (conteneur Docker dédié), jamais le shell de l'hôte prod.
- **Workspace dédié** hors des dépôts client et hors du socle.

## Déroulé

1. Confirmer le rôle : opérateur uniquement. Toute demande de faire exécuter du métier par Hermes → refuser et proposer l'orchestrateur AgenticOS.
2. Installer/configurer selon la checklist de durcissement, preuve par preuve.
3. Brancher Hermes sur la passerelle interne et vérifier qu'aucune clé fournisseur directe ne subsiste (`hermes config get`).
4. Vérifier la coexistence avec le skill `agenticos-audit` (maillon 2 — planification : aucun chemin parallèle créé par le cron Hermes).
