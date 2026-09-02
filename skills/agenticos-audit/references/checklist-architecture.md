# Checklist Architecture & Robustesse — AgenticOS / Hermes

## Sommaire
1. Chemins d'exécution
2. Passerelle LLM et routing
3. Mémoire et état
4. Gestion d'erreurs et fiabilité
5. Observabilité
6. Tests et reproductibilité

## 1. Chemins d'exécution (risque structurel n°1)
- [ ] Compter les voies d'exécution : scheduler hôte ∥ orchestrateur ∥ shadow crons. Objectif : **un seul chemin** (scheduler = enqueue-only → orchestrateur → worker sandboxé)
- [ ] Toute la sémantique (quotas, validation humaine, force_local, sandbox, deliver) vit à **un seul endroit** du code
- [ ] Shadow crons inventoriés (`crontab -l`), plan de migration un par un avec double-run de validation — jamais de big bang
- [ ] Aucun `run.py` lancé directement sur l'hôte pendant un run cron

## 2. Passerelle LLM et routing
- [ ] Passerelle unique (LiteLLM ou équivalent OpenAI-compatible), ≥ 2 réplicas, fallbacks configurés, retries, timeouts
- [ ] Chaîne de fallback cohérente : vérifier qu'un modèle `fast` n'est pas fallback de tout (dérive coût/qualité) ; exiger un graph coût/latence avant-après pour tout changement de chaîne
- [ ] Budgets mensuels par tenant + alerte à 80 % de consommation
- [ ] Tool calling natif privilégié sur parsing fragile (JSON structuré garanti par l'API) ; parser robuste (accolades équilibrées / json5) seulement en fallback pour modèles sans tool calling
- [ ] Décision ReAct : 100 exécutions de test sans échec de parsing

## 3. Mémoire et état
- [ ] État persistant entre runs : table `agent_state (tenant, agent, key, value JSONB, updated_at)` avec `tenant_id` NOT NULL
- [ ] Mémoire vectorielle : répartition par tenant vérifiable, recherche filtrée par tenant retournant les bons résultats
- [ ] Occupation mémoire < 60 % (alerte à 80 % — 95 % = saturation imminente)
- [ ] Politique de rétention : résumé des sessions > 30 j, archivage, cron de consolidation actif — sinon retour à saturation en ~3 mois
- [ ] Backup avant toute migration de données, avec test de restauration réel

## 4. Gestion d'erreurs et fiabilité
- [ ] Reaper au démarrage : exécutions `running > timeout → failed` (zombies)
- [ ] `error_detail = (stderr or stdout)[-2000:]` — taux d'échecs diagnosables > 90 %
- [ ] Idempotence : relancer un agent deux fois ne produit ni doublon ni double application
- [ ] Dégradation gracieuse : service externe down (LLM, Telegram, DB) → log + retry, jamais de crash du scheduler
- [ ] Bugs de scheduling : matcher DOW (décalage jour de semaine), fuseaux horaires

## 5. Observabilité
- [ ] Traces LLM systématiques (Langfuse ou équivalent) — **non désactivable**
- [ ] Dashboards : taux d'échec par agent, coût tokens par tenant, occupations mémoire, files d'attente, latence passerelle, saturation workers
- [ ] Vérification post-changement : le déclaré correspond à l'exécuté

## 6. Tests et reproductibilité
- [ ] Suite de tests existante verte après chaque phase de changement + tests des nouvelles preuves de fin
- [ ] CI : lint, validate (`terraform validate`, `kustomize build`), scan de secrets
- [ ] Un tiers peut reproduire le déploiement en suivant uniquement le README/runbook
- [ ] Runbook à jour : architecture réelle, redémarrage après crash, restauration backup, journal des migrations
