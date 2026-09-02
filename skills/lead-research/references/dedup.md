# Pattern de déduplication et validation des emails

## Sources de dédup

1. **Mémoire** (`search_memory("lead")`) — contacts déjà validés (kind=lead).
2. **Fichiers** — scraper-*.csv / *-contacts.json (read_file / list_files).
3. **Collectes** — scrape_status (fichiers produits), count_contacts (comptage).

## Règle de dédup

- Un contact est **doublon** si son email existe déjà (mémoire ou autre fichier).
- Un contact est **nouveau** s'il n'apparaît nulle part ailleurs.
- Un contact **invalidé** si email vide / mal formé / junk / champ manquant.

## Règle d'émails valides

- Format : `<local>@<domaine>` avec domaine non junk (noreply, example.com, webmaster@).
- Aucune validation par envoi réel (lecture seule) — la validation est structurelle.

## Sortie attendue

```
Contacts lus: N (fichiers: [...])
Nouveaux: N | Doublons: N | Invalidés: N
Emails valides: N
Rapport mémoire: kind=lead persisté
```
