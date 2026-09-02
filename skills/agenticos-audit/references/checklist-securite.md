# Checklist Sécurité — AgenticOS / Hermes

## Sommaire
1. Secrets et credentials
2. Contrôle d'accès et rôles
3. Exécution et sandbox
4. Réseau
5. Guardrails et données sensibles
6. Journal d'audit

## 1. Secrets et credentials
- [ ] Aucun secret en clair dans le dépôt (clés API, mots de passe, tokens) — scanner aussi l'historique git et les fichiers `.env` non chiffrés (sops attendu)
- [ ] Les logs et tables d'audit (`aos_audit`, guardrails) ne stockent pas de secrets : seuls `type + pos` doivent être conservés
- [ ] Secrets via coffre externe / External Secrets Operator (K8s) ; placeholders dans les fichiers d'exemple
- [ ] Mots de passe de consoles (Grafana, etc.) : forts, comptes locaux désactivés si SSO/OIDC disponible

## 2. Contrôle d'accès et rôles
- [ ] Rôle par défaut **fail-closed** (`viewer` / refus) — tester l'accès sans rôle explicite
- [ ] RBAC minimal : un ServiceAccount par composant, aucun `cluster-admin`
- [ ] PodSecurityStandards `restricted` sur les namespaces du socle
- [ ] Validation humaine : agents marqués `required` → pause effective + validation (Telegram/autre) ; `--auto-approve` jamais utilisé en prod ; l'approbation est liée au hash de l'action (non contournable par reformulation)

## 3. Exécution et sandbox
- [ ] Tout code généré par agents s'exécute en runtime isolé (gVisor / Firecracker / Kata / conteneur podman sandboxé)
- [ ] **Tous** les chemins d'exécution passent par le sandbox — un cron shadow ou un scheduler hôte qui lance du code directement = critique
- [ ] Variables d'environnement des workers pointant exclusivement vers la passerelle LLM interne

## 4. Réseau
- [ ] NetworkPolicy `deny-all` (ingress + egress) par défaut, ouvertures explicites uniquement (agents → passerelle `:4000`, agents → données `:5432/:6379/:6333`, DNS `:53/udp`)
- [ ] Aucun composant ne contacte un fournisseur LLM directement (passerelle unique obligatoire)
- [ ] Exposition externe minimale : consoles derrière SSO, pas de port d'admin ouvert

## 5. Guardrails et données sensibles
- [ ] `routing-policies.yaml` (ou équivalent) réellement chargé et appliqué **avant dispatch** : `block-secrets`, `s1-local-only`
- [ ] `force_local` enforcé au dispatch (refus + audit si modèle non local sur tenant concerné) — pas seulement affiché dans la console
- [ ] `check_output` branché sur tous les canaux de livraison (Telegram, email…) : contenu interdit → bloqué + audité
- [ ] Données S1 (copropriété, Loi 18.00 / RGPD-like) : localisation, chiffrement, cloisonnement par tenant (`tenant_id` NOT NULL dans toutes les tables métier et mémoire)

## 6. Journal d'audit
- [ ] Toute requête orchestrateur journalisée : qui, quoi, quand, coût
- [ ] Destination pérenne (table dédiée + export objet) ; idéalement hash-chainée
- [ ] Scan de l'historique : 0 secret en clair
