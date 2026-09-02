# Checklist Conformité Socle — AgenticOS / Hermes (K8s + Terraform)

À appliquer uniquement si l'infra auditée suit le socle Kubernetes/Terraform (passerelle LiteLLM, Kustomize base+overlays, Argo CD). Sinon, sauter cette checklist.

## Principes P1–P8 (non négociables)

| # | Principe | Vérification |
|---|---|---|
| P1 | Socle gelé | Aucune valeur client dans `base/` ni les modules Terraform ; tout vit dans overlays/tfvars |
| P2 | Passerelle LLM unique | Aucun composant ne contacte un fournisseur directement ; env des workers = passerelle interne uniquement |
| P3 | Exécution sandboxée | `runtimeClassName: gvisor` (ou équivalent) sur tous les workers |
| P4 | Cloisonnement réseau | NetworkPolicy `deny-all` sur `hermes-agents` et `hermes-data` + ouvertures explicites |
| P5 | Observabilité non désactivable | Aucune option ne désactive traces/métriques/audit ; callback Langfuse systématique |
| P6 | Aucun secret en clair | External Secrets / coffre ; scan CI de motifs de secrets |
| P7 | Déclaratif et reproductible | IaC uniquement, zéro étape manuelle requise |
| P8 | Rétro-compatibilité socle | Une personnalisation 1.x fonctionne sur toute version 1.y |

## Traçabilité exigences (EF / ENF)

- [ ] EF-02 Passerelle LiteLLM : `/v1/models` joignable via service interne, `/health/liveliness` OK
- [ ] EF-03 Mémoire : PostgreSQL 16 + Redis 7 (appendonly) + Qdrant — pods Ready, PVC bound
- [ ] EF-05 Budgets/quotas : patch overlay visible dans `kustomize build`, plafond HPA ajustable
- [ ] EF-06 Trace Langfuse visible après un appel de démo
- [ ] EF-07 Scaffolding : `nouveau-client.sh <nom>` refuse d'écraser un client existant, remplace les placeholders, overlay généré buildable
- [ ] EF-09 GPU : module `gpu-nodepool` optionnel (`count = enable_gpu ? 1 : 0`), vLLM fonctionnel si activé
- [ ] ENF-04 Sandbox + NetworkPolicies appliqués
- [ ] ENF-08 Budget mensuel + alerte 80 % configurés et documentés

## Contrat de configuration

- [ ] `config/values-communs.yaml` = source de vérité : `commun` (non surchargeable) / `modules_optionnels` / `personnalisable`
- [ ] Overlays et tfvars reflètent ces clés sans en inventer d'autres
- [ ] Backend d'état Terraform isolé par client (`backend.hcl` dédié)
- [ ] Tout écart à la stack imposée justifié par un ADR dans `docs/ADR-*.md`

## Méta-agents (si `agenticos-meta` présent)

- [ ] Read-only par défaut : écriture uniquement dans les tables `meta_*`
- [ ] Aucune mutation sans validation humaine horodatée (state machine `meta_proposals`)
- [ ] security-sentinel peut opposer un veto (`vetoed`)
- [ ] Jamais de code métier dans le socle ; agents générés écrits dans le package métier
- [ ] Suite de tests verte avec le package métier absent (non-régression)
