---
name: competitor-analysis
description: Expertise veille concurrentielle — mouvements notables, positionnements comparés, alertes. À charger AVANT toute mission de veille concurrentielle (agent competitor-watcher). Vérifier le nom exact du skill : 'competitor-analysis' (et non competitor-watcher).
version: 1.0.0
---

# Competitor Analysis — expertise veille concurrentielle

## Références à charger
- `references/mouvements-notables.md` — Grille de détection des mouvements
- `references/comparaison-positionnements.md` — Grille de comparaison

## Doctrine (rappel non-négociable)
- **Zéro invention** : chaque mouvement (lancement, prix, repositionnement) est
  prouvé par une source (veille, product_scan, mémoire).
- **Rigueur** : on compare sur des critères fixes, jamais sur une impression.
- **Silence utile** : pas d'alerte Telegram sans mouvement notable réel.
- **Mémoire** : persister l'analyse (kind=competitor) avant tout résumé.

## Workflow
1. `search_memory("concurrent")` — liste des concurrents suivis, analyses passées.
2. `veille_collect()` + `product_scan()` + `scrape_status()`.
3. Détecter les mouvements (grille) et comparer les positionnements.
4. `save_memory(kind="competitor", ...)` + résumé conforme au contrat de sortie.

## Pièges connus
- Un « mouvement » non vérifié est une rumeur — le dire, ne pas l'affirmer.
- Ne pas donner d'avis d'investissement (hors périmètre).
