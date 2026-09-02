---
name: klerbot-brand-voice
description: Voix de marque et positionnement editorial Klerbot.
version: 1.0.0
kind: context-tenant
family: klerbot
---

# Klerbot Brand Voice

## Type
Context skill — connaissance specifique au tenant Klerbot.

## Quand charger ce skill
Toujours AVANT une mission Klerbot dans le domaine correspondant.

## References a charger (dans l ordre)
- `references/context.md` — contexte Klerbot a injecter
- `references/constraints.md` — contraintes et conventions du tenant

## Doctrine
- **Zero invention** : chaque affirmation doit etre sourcee (memoire, outil, ou reference du skill).
- **No permissions** : ce skill fournit une methode, jamais une autorisation runtime.
- **Tenant context** : ce skill ne peut etre applique qu avec le contexte Klerbot ; il est inerte sans un agent du tenant klerbot.
- **Anti-doublon** : verifier `search_memory` avant de reproduire un resultat recent.
- **Format de sortie** : respecter le contrat de sortie de l agent consommateur.

## Workflow
1. Charger les references du skill.
2. Collecter les entrees via les outils autorises de l agent.
3. Appliquer la methode decrite dans la reference.
4. Produire une proposition / analyse / recommandation structuree.
5. Persister en memoire avec le `kind` conventionnel de l agent.

## Pieges connus
- Ne pas confondre methode et permission.
- Ne pas ecrire directement dans le repo produit sauf si l agent a explicitement un outil d ecriture autorise.
- Ne pas embarquer de secret, credential ou donnee PII dans le skill.

## Consommateurs attendus
- `klerbot-*` agents dans leur domaine respectif.
