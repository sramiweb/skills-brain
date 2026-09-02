# Passerelle LLM et routing — AgenticOS

## Sommaire
1. Passerelle unique
2. Chaînes de fallback
3. Budgets et quotas
4. Décision et tool calling
5. Preuves de fin

## 1. Passerelle unique

- LiteLLM (ou équivalent OpenAI-compatible) comme **point unique** d'accès LLM : tous les workers pointent vers elle, aucun ne contacte un fournisseur directement (principe P2, vérifié par NetworkPolicy).
- ≥ 2 réplicas derrière un service interne ; retries, timeouts et circuit breaker configurés.
- Healthchecks : `/health/liveliness` OK, `/v1/models` joignable via le service interne.
- Les agents référencent des **alias** (`fast`, `strong`, `local`), jamais des noms de fournisseurs — le mapping vit dans la config passerelle.

## 2. Chaînes de fallback

- Cohérence d'abord : un modèle `fast` fallback de tout = dérive coût/qualité. Chaque chaîne lie des modèles de classe comparable.
- Les tenants `force_local` (S1) ne doivent avoir **aucun** fallback vers un modèle externe — la chaîne s'arrête au local.
- Tout changement de chaîne : graph coût/latence avant-après obligatoire, tracé dans un ADR si l'écart est structurel.
- **Preuve** : couper le modèle principal en qualification → le trafic bascule sur le fallback attendu, et uniquement lui.

## 3. Budgets et quotas

- Budget mensuel par tenant + alerte à **80 %** de consommation (ENF-08), documentée et testée.
- Quotas par agent (`tokens_per_day`, `runs_per_day`) enforcés par l'orchestrateur, pas par la passerelle seule.
- **Preuve** : simuler une consommation à 81 % → alerte émise ; dépasser le quota d'un agent → refus journalisé.

## 4. Décision et tool calling

- **Tool calling natif** privilégié : JSON structuré garanti par l'API. Parser robuste (accolades équilibrées / json5) uniquement en fallback pour modèles sans tool calling.
- Exigence de fiabilité : 100 exécutions de test sans échec de parsing avant de considérer le maillon « décision » fiable.
- Approbation humaine liée au **hash de l'action** — une reformulation invalide l'approbation.

## 5. Preuves de fin

- Appel de démo → trace Langfuse visible, avec coût et latence.
- Panne passerelle simulée → workers en log + retry, scheduler vivant.
- Dashboard coût/latence par tenant alimenté en continu.
