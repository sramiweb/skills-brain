---
name: agenticos-eval
description: Évaluer les agents d'une infra AgenticOS/Hermes — golden tasks par agent, fiabilité du tool calling (100 exécutions sans échec de parsing), mesure coût/latence/qualité avant-après tout changement de modèle, de prompt ou de chaîne de fallback, détection de régression. À utiliser dès qu'on change un modèle, un prompt, un outil ou une politique de routing, ou qu'on veut prouver la fiabilité d'un agent (maillons décision et amélioration de la boucle d'autonomie). Mots-clés : eval, évaluation, golden dataset, régression, benchmark agent, avant/après.
---

# AgenticOS Eval

Sans évaluations, le maillon « amélioration » de la boucle d'autonomie repose sur l'intuition, et tout changement (modèle, prompt, fallback) est un pari. Règle d'or : **aucune modification d'un agent en prod sans mesure avant/après sur ses golden tasks**.

## Déroulé

1. **Définir les golden tasks** : partir de `assets/golden-tasks.yaml` — par agent, 10–30 cas représentatifs avec critères de réussite exécutables (pas « la réponse est bonne », mais « contient X / appelle l'outil Y / refuse Z »). Couvrir au minimum : cas nominal, cas limite, cas hostile (secret à bloquer, action interdite à refuser).
2. **Exécuter et enregistrer** : chaque run produit une ligne JSONL (`task_id, agent, success, parse_ok, cost_usd, latency_s, detail`). Viser 100 exécutions pour la fiabilité du parsing (exigence du maillon 3 — décision).
3. **Scorer** : utiliser `assets/eval-scoring.py` — calcule taux de succès, taux de parsing OK, coût et latence moyens/P95, et compare à une baseline.
4. **Comparer avant/après** : toute évolution se mesure contre la baseline du même agent : régression = succès en baisse, coût ou latence P95 en hausse > 20 %, ou parsing OK < 100 %. Une régression bloque la mise en prod.
5. **Tracer** : les résultats d'eval rejoignent le runbook et l'ADR du changement ; les traces détaillées restent dans Langfuse.

## Règles de conduite

- Les golden tasks sont versionnées avec l'agent, jamais modifiées pour faire passer un run (si une tâche est mauvaise, la corriger en la documentant).
- Données de test synthétiques ou anonymisées — jamais de S1 réel dans un dataset d'eval.
- Un agent sans golden tasks est noté « décision : non démontrée » dans l'audit — livrer les evals avec l'agent, pas après.
- Détailler les métriques et seuils : voir `references/metriques-et-seuils.md`.
