---
name: agenticos-securite
description: Implémenter la sécurité d'une infra AgenticOS/Hermes à la construction — secrets (sops/coffre/External Secrets), rôles fail-closed, sandbox gVisor, NetworkPolicy deny-all, validation humaine liée au hash, guardrails S1, journal d'audit sans secrets. À utiliser dès qu'on ajoute un agent, un outil, un canal de livraison ou un accès réseau, ou qu'on touche aux credentials, RBAC, sandbox ou données sensibles.
---

# AgenticOS Sécurité

Implémenter la sécurité **à la construction**, pas en rustine après audit. Chaque mesure ci-dessous correspond à un point chaud connu d'AgenticOS — les traiter dès le départ coûte des heures, les corriger après coup coûte des jours (ou un incident).

## Priorités Jour 0 (les 5 qui tuent)

1. **Rôle par défaut fail-closed** : tout accès sans rôle explicite = refus (`viewer` au mieux). Tester l'accès anonyme avant toute mise en route.
2. **Zéro secret en clair** : ni dans le dépôt (historique git compris), ni dans les logs/tables d'audit (`aos_audit` ne stocke que `type + pos`). Secrets via sops ou coffre externe.
3. **Tous les chemins d'exécution passent par le sandbox** : un shadow cron ou un scheduler hôte qui exécute du code directement contourne tout le reste — c'est le P0 structurel.
4. **Mots de passe consoles forts** : comptes locaux désactivés si SSO/OIDC disponible (Grafana, consoles d'admin).
5. **Code sous git avec remote** : aucun code de prod vivant uniquement sur une machine.

## Déroulé d'implémentation

1. **Charger** `references/checklist-implementation.md` et traiter chaque section comme une spec à implémenter avec sa preuve (test, commande, scan).
2. **Secrets** : partir de `assets/sops-et-external-secrets.yaml` (chiffrement au repos + injection coffre) et brancher `assets/gitleaks-ci.yml` en CI — scan bloquant du working tree et de l'historique.
3. **Réseau** : partir de `assets/networkpolicy-deny-all.yaml` — deny-all ingress+egress par défaut, ouvertures explicites uniquement (agents → passerelle `:4000`, agents → données, DNS).
4. **Admission et sandbox** : partir de `assets/pod-security-restricted.yaml` — PSS `restricted` sur les namespaces du socle + securityContext minimal des workers.
5. **Validation humaine** : implémenter selon `assets/approval-hash.py` — l'approbation est liée au **hash de l'action** ; toute reformulation l'invalide. `--auto-approve` interdit en prod.
6. **Guardrails** : `block-secrets` et `s1-local-only` enforcés **avant dispatch** ; `check_output` branché sur **tous** les canaux de livraison.
7. **Prouver** : pour chaque mesure, livrer le test négatif correspondant (action interdite → refus ; secret dans une tâche → blocage ; modèle externe sur S1 → deny + audit).

## Règles de conduite

- Ne jamais introduire un contournement « temporaire » (secret en clair, deny-all désactivé, sandbox contourné) sans accord explicite et daté de l'utilisateur, tracé dans un ADR.
- Prioriser par exploitabilité réelle : un secret en clair lu par un agent passe avant toute bonne pratique.
- Terminer en proposant une vérification croisée avec le skill `agenticos-audit` (checklist sécurité).
