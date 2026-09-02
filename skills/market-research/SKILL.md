---
name: market-research
description: Expertise marché SaaS — collecte, croisement de sources, positionnement, recommandations produits. À charger AVANT toute mission de synthèse marché (agent market-researcher). Vérifier le nom exact du skill : 'market-research' (et non market-researcher).
version: 1.0.0
---

# Market Research — expertise marché SaaS

## Références à charger (dans l'ordre)
- `references/criteres-signaux.md` — Grille de lecture des signaux (croissance/risque/opportunité/déclin)
- `references/positionnement.md` — Cadre de positionnement (cible, prix, différenciation)
- `references/methodologie.md` — Workflow de synthèse (croiser ≥2 sources, jamais conclure sur une seule)

## Doctrine (rappel non-négociable)
- **Zéro invention** : chaque chiffre, tendance ou produit vient d'un outil réel
  (veille_collect, product_scan, scrape_status, read_file) ou de la mémoire
  (search_memory). Un signal non vérifié est signalé comme tel, jamais affirmé.
- **Doublon** : si un sujet a déjà été traité dans les 7 derniers jours
  (search_memory), le signaler et ne pas le retraiter à fond.
- **Défaut de source** : si les collectes sont dégradées (erreur, vide, 401),
  le dire en clair dans la synthèse et s'appuyer sur la mémoire fiable.
- **Règle de sortie** : pas de notification Telegram sans nouveau actionnable ;
  la synthèse complète est toujours persistée en mémoire (kind=market).

## Workflow recommandé
1. `search_memory("market")` — synthèses précédentes, doublons.
2. `veille_collect()` — tendances 24h ; `product_scan()` — produits digitaux ;
   `scrape_status()` — état des collectes scraper.
3. Croiser ≥2 sources avant de conclure.
4. `save_memory(kind="market", ...)` + résumé final conforme au contrat de sortie.

## Pièges connus
- product_scan peut revenir vide (401, clé expirée) — ne pas inventer de produit.
- Les collectes scraper peuvent être absentes — le signaler, ne pas inventer.
- Ne jamais copier une réponse : chaque synthèse est rédigée dans ses propres mots.
