---
name: lead-research
description: Expertise enrichissement et déduplication de leads B2B — ICP, validation emails, fichiers scraper. À charger AVANT toute mission de recherche de leads (agent lead-researcher). Vérifier le nom exact du skill : 'lead-research' (et non lead-researcher).
version: 1.0.0
---

# Lead Research — expertise recherche de leads B2B

## Références à charger
- `references/icp.md` — ICP KlerBot (fiduciaires marocaines, fleet DE) et critères de validation
- `references/dedup.md` — Pattern de déduplication et de validation des emails

## Doctrine (rappel non-négociable)
- **Zéro invention** : un contact/email/chiffre vient d'un fichier réel
  (scrape_status, count_contacts, list_files, read_file) ou de la mémoire
  (search_memory). Jamais un contact inventé.
- **Lecture seule** : ne pas modifier les fichiers de collecte (dédup = rapport,
  pas d'écriture).
- **Défaut de collecte** : si aucun fichier (0 contact), le signaler en clair
  (avec récidives documentées en mémoire) — pas de fabrication.
- **Rapport** : persister en mémoire (kind=lead) avant tout résumé.

## Workflow
1. `search_memory("lead")` — contacts validés, historique de dédup.
2. `scrape_status()` + `count_contacts()` + `list_files()` + `read_file()`.
3. Dédupliquer (référence dédup.md), valider les emails (format + mémoire).
4. `save_memory(kind="lead", ...)` + rapport conforme au contrat de sortie.

## Pièges connus
- 401 LLM du scraper = blocage racine récurrent — le signaler avec compteur
  de récidives (déjà documenté en mémoire, 8e récidive 19/08).
- Ne jamais valider un email sans source (pas de supposition).
