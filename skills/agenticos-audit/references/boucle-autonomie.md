# Boucle d'autonomie — grille des 9 maillons

L'audit de l'autonomie porte sur ce qui est **démontré en exécution**, jamais sur la seule présence de configuration. Chaque maillon est noté **présent / partiel / absent** avec sa preuve.

Boucle : `déclaration → planification → décision → appel outils → observation → mémoire → coordination → reprise → amélioration`

## Grille par maillon

| # | Maillon | Question d'audit | Preuve exigée | Piège connu à tester |
|---|---|---|---|---|
| 1 | **Déclaration** | L'agent déclaré (`agents.yaml`) correspond-il à ce qui s'exécute ? | Diff YAML ↔ runtime : modèle, outils, quotas, `force_local`, `human_validation` | YAML qui ment : politique déclarée jamais chargée par le code |
| 2 | **Planification** | Qui déclenche réellement l'agent ? | Trace d'un run : scheduler → enqueue → orchestrateur | Chemins parallèles : shadow crons, `run.py` sur l'hôte contournant l'orchestrateur ; bug DOW (décalage jour de semaine) |
| 3 | **Décision** | Le raisonnement est-il structuré et fiable ? | 100 exécutions sans échec de parsing ; approbation liée au hash de l'action | Parser ReAct fragile vs tool calling natif ; approbation contournable par reformulation |
| 4 | **Appel outils** | Les outils (MCP, SQL, HTTP, fichiers) sont-ils réellement invoqués, avec garde-fous ? | Trace d'appel outil + test négatif (outil/action interdit → refus) | Routage non enforcé (`block-secrets`, `s1-local-only` avant dispatch ?) ; sandbox effectif sur code généré |
| 5 | **Observation** | L'agent perçoit-il résultats et erreurs ? | `error_detail = (stderr or stdout)[-2000:]` ; trace Langfuse de la boucle complète | Échecs silencieux ; taux d'échecs diagnosables < 90 % |
| 6 | **Mémoire** | L'agent se souvient-il entre les runs ? | Run N+1 relit l'état du run N (`agent_state`) ; recherche mémoire filtrée par tenant | `tenant_id` NULL ; occupation > 80 % sans politique de rétention ; fuite inter-tenant |
| 7 | **Coordination** | Les agents se coordonnent-ils sans conflit ? | File de tâches, verrous, pas de double exécution ; inter-tenant interdit par défaut | Deux chemins exécutant le même agent en doublon ; couplage sauvage hors contrat |
| 8 | **Reprise** | Que se passe-t-il après échec ou crash ? | Reaper (zombie `running > timeout → failed`), retry avec backoff, scheduler ne crash jamais | Exécutions orphelines ; perte de travail au redémarrage ; migration en big bang |
| 9 | **Amélioration** | Le système apprend-il de ses propres exécutions ? | Proposition (`meta_*`) traçable, validée humainement, vérifiée après application | Auto-modification sans veto humain ; spécifié ≠ codé ≠ opérationnel (agenticos-meta) |

## Méthode d'application

1. **Échantillon d'agents tracés** : au moins 3 profils représentatifs — un agent planifié simple (ex. `sre-health`), un agent à données sensibles S1 (ex. `syndic-rapporteur`), un agent à action externe risquée (ex. `outreach-operator`). Les maillons 3, 4 et 9 ne se prouvent que sur du réel.
2. **Test de bout en bout** : suivre une exécution complète d'un agent, du déclencheur à la livraison, en annotant chaque maillon avec sa preuve (trace, log, audit).
3. **Test négatif par maillon quand applicable** : action interdite → refus ; modèle non conforme sur tenant `force_local` → blocage ; contenu interdit → non livré.

## Règles de notation

- Un maillon est **présent** uniquement s'il est démontré en exécution (trace, log, audit, test négatif réussi) — jamais sur déclaration.
- **Une chaîne vaut son maillon le plus faible** : agent parfaitement déclaré mais lancé par un shadow cron hors sandbox = autonomie **non démontrée** pour cet agent.
- Résultat par agent audité : 9 notes de maillon + un schéma de la boucle réellement observée, mettant en évidence les maillons contournés.
- Tout maillon **absent** ou **partiel** devient un finding au format de `grille-scoring.md` (constat → preuve → risque → recommandation → effort).
