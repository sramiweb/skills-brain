# Méthodologie de synthèse marché

## Workflow (dans l'ordre)

1. **Contexte** : `search_memory("market")` — synthèses précédentes, décisions, doublons.
2. **Collecte** : `veille_collect()` + `product_scan()` + `scrape_status()` — en parallèle.
3. **Qualification** : appliquer `criteres-signaux.md` (croiser ≥2 sources).
4. **Positionnement** : appliquer `positionnement.md` (cible/besoin/prix/différenciation).
5. **Persistance** : `save_memory(kind="market", title="Synthèse marché hebdo <date>", content="<résultat structuré>")`.
6. **Livraison** : résumé final conforme au contrat de sortie (5-7 lignes, chiffres clés en tête) ; Telegram uniquement si nouveau actionnable.

## Règles d'or

- **Zéro invention** : tout chiffre vient d'un outil ou de la mémoire.
- **Dégradation assumée** : si une source échoue (erreur/vide/401), le dire dans
  la synthèse, s'appuyer sur la mémoire fiable, et ne pas inventer de complément.
- **Synthèse personnelle** : pas de copier-coller — reformuler avec ta valeur ajoutée
  (mise en perspective, implications business).
- **Ne pas conclure sur une source unique** : croiser avant d'affirmer.
