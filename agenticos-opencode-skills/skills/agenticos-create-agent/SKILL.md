---
name: agenticos-create-agent
description: Workflow opérationnel de création d'un agent AgenticOS — validation du nom, create-agent.sh, édition du prompt selon les règles manifest (tout outil cité = manifest + policy, sinon refus serveur), ajout de la règle policy, régénération du skill-manifest via script (jamais à la main), --check à 0 drift, dry-run scheduler. À utiliser dès qu'on crée ou ajoute un nouvel agent dans une infra AgenticOS. Mots-clés : créer un agent, nouvel agent, create-agent, manifest, policy, dry-run.
---

# AgenticOS — Création d'un agent

Créer un agent dont le **déclaré dit la vérité dès la naissance** : prompt, manifest et policy alignés, vérifiés par `--check`, et visibles par le scheduler — sans aucune écriture manuelle dans les fichiers générés.

## Séquence (dans cet ordre, sans en sauter)

0. **Vérifier les patterns existants AVANT de scaffolder** (leçon 23/08 — P1/P2 pitfalls money) :
   - `~/workspace/syndic-manager/` — pattern domaine dédié (SQLite `data/syndic.db` + skill Hermes + scripts) ;
   - Gateway Hermes (`~/.hermes/`) — reçoit DÉJÀ les messages Telegram (pattern syndic : parsing + exécution) ;
   - `~/.hermes/memories/MEMORY.md` — règles datées ("jamais contourner Hermes", "enqueue OBLIGATOIRE") ;
   - Skills Hub (`~/.hermes/skills/`) et skills agenticos-* (`~/.config/opencode/skills/`).
   Ne jamais supposer qu'un mécanisme n'existe pas.
1. **Validation du nom** : verbe-domaine (`sre-health`, `syndic-rapporteur`), unique dans `agents/`, refus d'écraser un agent existant. Tenant et classe de données (S0/S1) décidés **avant** d'écrire quoi que ce soit — ils conditionnent tout le reste.
2. **`create-agent.sh <nom>`** : scaffolding officiel uniquement. Jamais de copier-coller d'un agent existant comme base (il hérite de ses outils fantômes et de ses écarts).
3. **Édition du prompt** : suivre `references/regles-manifest.md` — tout outil cité dans le prompt doit exister dans le manifest de l'agent **et** dans la policy, sinon le serveur le refusera. Ne jamais citer `run_script` (supprimé). Renseigner les deux catalogues : Prod (outils du manifest) et Dev local (liste limitée, test explicite uniquement).
4. **Règle policy** : ajouter la règle de l'agent dans `policy.yaml` avec `skill_id` explicite, tenants et outils restreints au nécessaire (modèle : la règle `memory-keeper`). Chaque nouvelle règle exige son **test négatif** : un tenant ou un outil hors liste → refus prouvé.
5. **Régénération du manifest** : `python3 scripts/skill-manifest.py` — jamais d'édition manuelle de `manifest.yaml`.
6. **`--check = 0 drift`** : tout écart prompt ↔ manifest ↔ policy bloque la création.
7. **Dry-run scheduler** : vérifier que l'agent est planifiable et enqueue correctement (matcher DOW, fuseau), sans exécution réelle. Preuve : ligne d'enqueue en dry-run, aucune exécution.

## Garde-fous (non négociables)

- **Approbation humaine avant toute écriture** dans `policy.yaml` ou le manifest régénéré : présenter le diff, attendre le accord explicite. Pas d'écriture silencieuse dans les fichiers de contrôle.
- **Cohérence D1** : pas d'agent à appels d'outils sur un tenant `force_local` tant que le modèle local n'a pas de tool calling fiable — un tel agent resterait bloqué en prod par le routing S1 (limitation connue, documentée). Si le besoin existe, le traiter comme une décision datée (modèle local avec tool calling via vLLM, ou report), pas comme un oubli.
- **Un seul chemin d'exécution** : le nouvel agent n'est lancé que via le scheduler enqueue-only → orchestrateur. Pas de `run.py` hôte hors test dev explicite et encadré.
- **Preuves de fin** : `--check` à 0 drift, dry-run scheduler réussi, test négatif de la règle policy vert. Sans ces trois preuves, l'agent n'est pas créé — il est déclaré.
- **Golden tasks** : livrer le squelette d'eval avec l'agent (voir `agenticos-eval`) — un agent sans golden tasks sera noté « décision : non démontrée » à l'audit.
