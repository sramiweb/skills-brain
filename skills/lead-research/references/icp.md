# ICP KlerBot et critères de validation

## Profils cibles (ICP)

| Segment | Critères | Exemples |
|---|---|---|
| **Fiduciaires marocaines** | cabinets comptables, PME/TPE, comptabilité/pre-comptabilité | klerbot-comptabilite-maroc |
| **Fleet DE** | entreprises de transport/flotte allemandes | fleet-de |

## Validation d'un contact

- **Email** : format valide (regex simple), pas de `noreply`, `example.com`,
  `webmaster@` ni domaines junk (liste des `JUNK_PATTERNS` du scraper).
- **Doublon** : email déjà présent dans la mémoire (kind=lead) → doublon, pas de revalidation.
- **Complétude** : nom/email/entreprise présents ; sinon « invalidé » avec motif.

## Règles

- Un contact non validé n'est jamais présenté comme valide.
- Le rapport distingue : lus / nouveaux / doublons / invalidés / emails valides.
