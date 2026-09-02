# Sécurité AgenticOS — checklist d'implémentation

Chaque item = mesure à implémenter + preuve exécutable attendue. Ne pas cocher sur déclaration.

## Sommaire
1. Secrets et credentials
2. Contrôle d'accès et rôles
3. Exécution et sandbox
4. Réseau
5. Guardrails et données sensibles
6. Journal d'audit

## 1. Secrets et credentials

- [ ] Secrets chiffrés au repos (sops) ou coffre externe / External Secrets Operator. **Preuve** : scan du dépôt + historique git (`gitleaks` ou équivalent) = 0 finding ; `.env.example` avec placeholders uniquement.
- [ ] Tables d'audit et guardrails ne stockent jamais de valeur de secret — seuls `type + pos`. **Preuve** : test injectant un faux secret dans une tâche → la table d'audit contient le type et la position, pas la valeur.
- [ ] Consoles (Grafana, admin) : mots de passe forts, comptes locaux désactivés si SSO/OIDC. **Preuve** : tentative de login local désactivé → refus.

## 2. Contrôle d'accès et rôles

- [ ] Rôle par défaut **fail-closed** (`viewer` / refus) — ex. variable `AOS_DEFAULT_ROLE` jamais fail-open. **Preuve** : accès sans rôle explicite → 403.
- [ ] RBAC minimal : un ServiceAccount par composant, aucun `cluster-admin`. **Preuve** : `kubectl auth can-i --list` par SA ne montre que le nécessaire.
- [ ] PodSecurityStandards `restricted` sur les namespaces du socle. **Preuve** : pod non conforme → rejeté à l'admission.
- [ ] Validation humaine bloquante pour agents `required` : pause effective + approbation liée au hash de l'action. **Preuve** : modifier le texte de l'action après approbation → exécution refusée ; `--auto-approve` absent des scripts de prod.

## 3. Exécution et sandbox

- [ ] Code généré par agents exécuté en runtime isolé (`runtimeClassName: gvisor` / Kata / Firecracker / conteneur sandboxé). **Preuve** : workload worker porte le runtimeClass ; test d'échappement basique (accès hôte) → échec.
- [ ] **Tous** les chemins d'exécution passent par le sandbox. **Preuve** : inventaire `crontab -l` + systemd timers = aucun lanceur d'agent hors orchestrateur.
- [ ] Env des workers : passerelle LLM interne uniquement. **Preuve** : `env` d'un pod worker ne contient aucune URL de fournisseur LLM ni clé API directe.

## 4. Réseau

- [ ] NetworkPolicy `deny-all` ingress+egress par défaut (base : `assets/networkpolicy-deny-all.yaml`), ouvertures explicites : agents → passerelle `:4000`, agents → données `:5432/:6379/:6333`, DNS `:53/udp`. **Preuve** : depuis un pod agent, `curl` vers Internet → timeout ; vers la passerelle → OK.
- [ ] Aucun composant ne contacte un fournisseur LLM directement. **Preuve** : logs egress / test de connectivité directe → bloqué.
- [ ] Exposition externe minimale : consoles derrière SSO, aucun port d'admin ouvert. **Preuve** : scan des services `LoadBalancer`/`NodePort` = liste vide ou justifiée par ADR.

## 5. Guardrails et données sensibles

- [ ] `routing-policies.yaml` chargé et appliqué **avant dispatch**. **Preuve** : test négatif par politique (`block-secrets` → deny ; tenant S1 vers modèle externe → deny + audit).
- [ ] `force_local` enforcé au dispatch, pas seulement affiché en console. **Preuve** : dispatch d'un agent S1 avec modèle externe → refus journalisé.
- [ ] `check_output` sur tous les canaux de livraison (Telegram, email…). **Preuve** : livraison d'un contenu interdit → bloquée + auditée.
- [ ] Données S1 : `tenant_id` NOT NULL dans toutes les tables métier et mémoire, chiffrement, localisation documentée. **Preuve** : tentative d'insert sans `tenant_id` → erreur contrainte ; requête cross-tenant → 0 ligne.

## 6. Journal d'audit

- [ ] Toute requête orchestrateur journalisée : qui, quoi, quand, coût. **Preuve** : exécution d'un agent → ligne d'audit complète.
- [ ] Destination pérenne (table dédiée + export objet), idéalement hash-chainée. **Preuve** : export présent et rejouable.
- [ ] Scan de l'historique d'audit : 0 secret en clair. **Preuve** : scan automatisé en CI.
