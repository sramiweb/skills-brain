---
name: release-readiness
description: Methode d evaluation de l etat de readiness d une release logicielle.
version: 1.0.0
kind: method-generic
family: engineering
---

# Release Readiness

## Type
Generic method — methode reutilisable independamment du tenant.

## Quand charger ce skill
Charger AVANT d evaluer si une version peut etre publiee.

## References a charger (dans l ordre)
- `references/methodology.md` — workflow standard
- `references/examples.md` — exemples de sortie

## Doctrine
- **Zero invention** : chaque critere doit etre verifiable (tests, PR, tickets, checklist).
- **No permissions** : ce skill fournit une methode, jamais une autorisation runtime.
- **Tenant context** : ce skill reste generique ; le contexte tenant (Klerbot) est injecte par l agent via agents.yaml ou sa memoire.
- **Anti-doublon** : verifier `search_memory` avant de reproduire une analyse de readiness.
- **Format de sortie** : verdict structuré GO / CONDITIONAL / NO-GO avec preuves.

## Workflow
1. Charger les references du skill.
2. Collecter l etat des PR, tests, tickets bloquants, documentation, rollback plan.
3. Appliquer la checklist `references/methodology.md`.
4. Produire un verdict avec actions correctives priorisees.
5. Persister en memoire avec le `kind` conventionnel de l agent.

## Pieges connus
- Ne pas confondre methode et permission.
- Ne jamais declencher un deploiement depuis ce skill.
- Ne pas embarquer de secret, credential ou donnee PII dans le skill.

## Consommateurs attendus
- `klerbot-qa-engineer`, `klerbot-release-manager`
