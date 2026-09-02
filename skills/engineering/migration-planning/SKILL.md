---
name: migration-planning
description: Methode de planification d une migration technique.
version: 1.0.0
kind: method-generic
family: engineering
---

# Migration Planning

## Type
Generic method — methode reutilisable independamment du tenant.

## Quand charger ce skill
Charger AVANT d executer la mission correspondante.

## References a charger (dans l ordre)
- `references/methodology.md` — workflow standard
- `references/examples.md` — exemples de sortie

## Doctrine
- **Zero invention** : chaque affirmation doit etre sourcee (memoire, outil, ou reference du skill).
- **No permissions** : ce skill fournit une methode, jamais une autorisation runtime.
- **Tenant context** : ce skill reste generique ; le contexte tenant (Klerbot) est injecte par l agent via agents.yaml ou sa memoire.
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
