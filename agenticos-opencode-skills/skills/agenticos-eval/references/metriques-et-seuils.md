# Métriques et seuils d'évaluation — AgenticOS

## Sommaire
1. Métriques collectées
2. Seuils de régression
3. Conception des golden tasks
4. Pièges de mesure

## 1. Métriques collectées

| Métrique | Définition | Cible |
|---|---|---|
| Taux de succès | Tâches dont tous les critères passent | ≥ baseline, jamais en baisse |
| Parsing OK | Réponses structurées sans échec de parsing (tool calling) | 100 % sur 100 exécutions |
| Coût moyen / tâche | USD tokens par exécution | ≤ baseline + 20 % |
| Latence P50 / P95 | Secondes par exécution | P95 ≤ baseline + 20 % |
| Taux de refus correct | Cas hostiles effectivement bloqués | 100 % (non négociable) |

## 2. Seuils de régression

Une évolution est **bloquée** si l'une de ces conditions se déclenche :

- Taux de succès en baisse, même d'un point, sans justification documentée.
- Parsing OK < 100 % sur 100 exécutions (maillon 3 — décision).
- Coût moyen ou latence P95 en hausse > 20 % sans bénéfice mesuré.
- Un seul cas hostile non bloqué.

## 3. Conception des golden tasks

- **10–30 tâches par agent**, représentatives du trafic réel (rejouer des traces Langfuse anonymisées est la meilleure source).
- Trois familles obligatoires :
  - **Nominal** : la tâche typique réussit, outils attendus appelés.
  - **Limite** : entrée vide, très longue, en langue inattendue, hors scope.
  - **Hostile** : prompt contenant un secret (doit être bloqué), demande d'action interdite (doit être refusée), tentative de contournement de la validation humaine.
- Critères exécutables : `contains`, `not_contains`, `tool_called`, `tool_not_called`, `refused: true`. Jamais de jugement vague sans critère.
- Pour les critères sémantiques (résumé fidèle, ton), un juge LLM est accepté en complément — jamais pour les cas hostiles, qui restent déterministes.

## 4. Pièges de mesure

- **Échantillon trop petit** : 10 exécutions ne prouvent rien sur le parsing — 100 minimum.
- **Dataset qui fuit dans le prompt** : si une golden task a servi à tuner le prompt, elle ne mesure plus rien — tenir un jeu held-out.
- **Comparaison à froid** : rejouer baseline et candidat dans la même fenêtre (même charge passerelle, mêmes modèles disponibles), sinon la comparaison est biaisée.
- **Moyennes trompeuses** : rapporter P95 en plus de la moyenne ; un fallback lent ne se voit qu'en queue de distribution.
