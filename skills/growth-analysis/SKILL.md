---
name: growth-analysis
description: Expertise analyse de croissance — signaux produits/veille, opportunités chiffrées, rapport hebdo. À charger AVANT toute mission de rapport croissance (agent growth-analyst). Vérifier le nom exact du skill : 'growth-analysis' (et non growth-analyst).
version: 1.0.0
---

# Growth Analysis — expertise croissance

## Références à charger
- `references/cadre-opportunites.md` — Cadre d'identification des opportunités chiffrées
- `references/rapport-hebdo.md` — Structure du rapport hebdomadaire

## Doctrine (rappel non-négociable)
- **Zéro invention** : chaque opportunité est justifiée par des données réelles
  (veille_collect, product_scan, scrape_status, mémoire). Une opportunité non
  chiffrable = signalée comme « non quantifiable », jamais inventée.
- **Données dégradées** : si les sources échouent, livrer une synthèse partielle
  honnête (pas d'opportunité fabriquée).
- **Mémoire** : persister le rapport en kind=growth avant tout résumé.

## Workflow
1. `search_memory("growth")` — rapports précédents, décisions.
2. `veille_collect()` + `product_scan()` + `scrape_status()`.
3. Appliquer le cadre d'opportunités (≥2 sources).
4. `save_memory(kind="growth_report", ...)` + résumé conforme au contrat de sortie.

## Pièges connus
- Ne pas confondre « signaux » et « opportunités » : une opportunité est chiffrée
  (marché, prix, demande) ou explicitement non quantifiable.
- product_scan en 401 → pas de recommandation fraîche, s'appuyer sur la mémoire.
