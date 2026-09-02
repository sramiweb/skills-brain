# Durcissement Hermes Agent — checklist d'intégration AgenticOS

Chaque item = mesure + preuve exécutable. Ne pas cocher sur déclaration.

## Sommaire
1. Accès et identité
2. LLM et secrets
3. Skills et code tiers
4. Exécution et données
5. Scheduler et chemins parallèles

## 1. Accès et identité

- [ ] Gateway messagerie (Telegram/Discord/Slack) restreinte : DM pairing activé, liste explicite d'utilisateurs autorisés. **Preuve** : message d'un compte non listé → ignoré/refusé.
- [ ] Approval des commandes activé : toute commande shell hors allowlist demande confirmation. **Preuve** : commande non approuvée → non exécutée, trace conservée.
- [ ] Allowlist de commandes minimale : pas de wildcard large (`*`, `sudo *`). **Preuve** : revue du fichier d'allowlist, aucun motif large.

## 2. LLM et secrets

- [ ] Provider Hermes = endpoint OpenAI-compatible de la passerelle AgenticOS (LiteLLM interne). **Preuve** : `hermes config get` montre l'URL interne ; test de connectivité directe vers un fournisseur → bloqué par NetworkPolicy.
- [ ] Aucune clé fournisseur (OpenAI, OpenRouter, Anthropic…) dans la config Hermes. **Preuve** : scan gitleaks de `~/.hermes` = 0 finding.
- [ ] Aucun credential prod (DB, admin, tokens client) accessible au process Hermes. **Preuve** : `env` du conteneur Hermes listé et revu ; secrets injectés depuis le coffre avec scope opérateur.

## 3. Skills et code tiers

- [ ] Confiance limitée aux skills du workspace projet, revues en PR comme tout code. **Preuve** : liste des skills actives = liste approuvée versionnée.
- [ ] Quarantaine du Skills Hub : tout skill tiers téléchargé est relu (code + instructions) avant activation. **Preuve** : procédure documentée + journal des revues ; un skill non relu n'est jamais activé.
- [ ] La boucle d'auto-création de skills d'Hermes écrit uniquement dans le workspace opérateur — jamais dans le socle ni les packages métier. **Preuve** : chemins de skills configurés hors dépôts client.

## 4. Exécution et données

- [ ] Backend d'exécution = conteneur dédié (Docker/Modal/Daytona), pas le shell de l'hôte. **Preuve** : terminal backend configuré ; une commande destructive test reste confinée.
- [ ] Données S1 interdites : ni en entrée de conversation, ni en mémoire (`MEMORY.md`, `USER.md`, SQLite). **Preuve** : scan périodique des fichiers mémoire ; règle inscrite dans le contexte projet d'Hermes.
- [ ] Workspace Hermes dédié, hors dépôts client et hors socle. **Preuve** : `hermes config get` working dir = chemin dédié.

## 5. Scheduler et chemins parallèles

- [ ] Le cron Hermes ne lance que des tâches opérateur (rappels, rapports internes). **Preuve** : liste des crons Hermes revue, aucune n'exécute du code métier/client.
- [ ] Aucun doublon avec le scheduler AgenticOS : une même tâche n'existe pas des deux côtés. **Preuve** : inventaire croisé des deux schedulers — 0 recouvrement.
- [ ] Toute action d'Hermes sur l'infra (déploiement, lecture de logs prod…) passe par les outils audités, avec identité opérateur. **Preuve** : une action test apparaît dans le journal d'audit AgenticOS.
