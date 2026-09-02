# Critères de lecture des signaux marché

Utilisés par l'agent market-researcher (et réutilisables par growth-analyst /
competitor-watcher) pour qualifier un signal collecté.

## 1. Catégories de signal

| Signal | Indicateurs | Action |
|---|---|---|
| **Croissance** | adoption en hausse, usage-based pricing, expansion géographique, MRR croissant | Recommander (opportunité) |
| **Risque** | consolidation, régulation, churn élevé, dépendance plateforme | Alerter (avec preuve) |
| **Opportunité** | gap de fonctionnalité, niche sous-servie, douleur exprimée, demande non satisfaite | Recommander (chiffrée si possible) |
| **Déclin** | intérêt en baisse, fermetures, départ de fondateurs, signaux de lassitude | Signaler (avec preuve) |

## 2. Preuve requise

- Un signal n'est qualifié que s'il est vérifiable : source (subreddit, HN,
  ProductHunt, fichier), chiffre, date.
- Pas de signal sans source identifiable → le mentionner dans l'analyse comme
  « non vérifié », jamais l'affirmer.
- Un chiffre cité = montant/rang/probabilité exact tiré d'un outil.

## 3. Croisement de sources

- Au moins **2 sources différentes** avant de conclure (ex. veille + mémoire,
  ou veille + product_scan).
- Si une seule source fiable : conclure avec prudence, le dire.
- Si aucune source fiable : synthèse « données indisponibles », pas d'invention.

## 4. Seuils de nouveauté

- Sujet traité dans les 7 jours (search_memory) → signaler, ne pas retraiter.
- Doublon détecté → notifier « doublon potentiel », ne pas recréer le livrable.
