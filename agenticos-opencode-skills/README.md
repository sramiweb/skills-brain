# Pack de skills AgenticOS pour opencode

Dix skills au format standard `SKILL.md` pour construire, sécuriser, opérer et auditer une infrastructure agentique AgenticOS/Hermes depuis opencode.

## Contenu du pack

| Skill | Rôle | Quand il se déclenche |
|---|---|---|
| `agenticos-scaffold` | Scaffolder l'infra : structure de dépôt, `agents.yaml`, `routing-policies.yaml`, orchestrateur, scheduler enqueue-only | Initialiser une infra, ajouter un tenant, une politique de routage |
| `agenticos-create-agent` | Workflow opérationnel de création d'agent : validation du nom → create-agent.sh → prompt aligné manifest → règle policy → skill-manifest.py → `--check` → dry-run scheduler, avec approbation humaine avant toute écriture policy/manifest | Créer ou ajouter un nouvel agent |
| `skill-creator` | Concevoir, créer, étendre ou refactorer un `SKILL.md`, avec détection de doublon, périmètre négatif et validation L1/L2 | Créer ou modifier un Agent Skill |
| `agenticos-securite` | Implémenter la sécurité à la construction : secrets, fail-closed, sandbox, NetworkPolicy, guardrails S1, audit log | Ajout d'outil, de canal de livraison, d'accès réseau, gestion de credentials/RBAC |
| `agenticos-memoire` | Mémoire et auto-apprentissage : `agent_state`, Qdrant par tenant, rétention, tables `meta_*` avec validation humaine | Persistance inter-runs, mémoire vectorielle, méta-agents |
| `agenticos-deploiement` | Socle et opérations : passerelle LiteLLM, fallbacks, budgets, reaper, observabilité, socle K8s/Terraform (P1–P8) | Déploiement, monitoring, runbook |
| `agenticos-eval` | Évaluer les agents : golden tasks, fiabilité du parsing (100 exécutions), mesure avant/après, blocage en cas de régression | Changement de modèle, de prompt, d'outil ou de fallback |
| `agenticos-migration` | Migrer sans big bang : inventaire des chemins, strangler, double-run, bascule item par item, décommissionnement | Sortir l'exécution métier d'Hermes, remplacer scheduler/passerelle/store |
| `agenticos-hermes-integration` | Hermes Agent (NousResearch) comme agent opérateur : passerelle interne, durcissement, quarantaine des skills, interdiction S1 | Installer/configurer Hermes aux côtés d'AgenticOS |
| `agenticos-audit` | Auditer l'infra : boucle d'autonomie (9 maillons), sécurité, robustesse, conformité socle, rapport priorisé P0/P1/P2 | Audit, revue, diagnostic d'autonomie ou de risques |

Les skills de construction, d'évaluation et de migration partagent les mêmes concepts (boucle des 9 maillons, points chauds Jour 0, principes P1–P8) : ce que les skills de construction implémentent est exactement ce que l'audit contrôle. `skill-creator` est un skill méta pour OpenCode et n'est pas une entrée du manifeste runtime des workers.

## Installation

### Dans une infra AgenticOS (versionné avec le dépôt)

```bash
cd /chemin/vers/votre/infra-agenticos
cp -r agenticos-opencode-skills/skills/* .agents/skills/
```

### En global (disponible dans tous vos projets)

```bash
mkdir -p ~/.config/opencode/skills
cp -r agenticos-opencode-skills/skills/* ~/.config/opencode/skills/
```

> Le chemin global est bien `~/.config/opencode/skills/` (pas `~/.opencode/skills/`). opencode lit aussi `.claude/skills/` et `.agents/skills/` si vous partagez les skills avec d'autres agents.

`skill-creator` est installé dans `.agents/skills/` pour l'infra et dans
`~/.config/opencode/skills/` pour l'utilisation globale avec OpenCode. Il ne
doit pas être ajouté à `modules/skill-registry/manifest.yaml` : ce manifeste
répertorie les skills exécutables par les workers.

## Vérification

Au démarrage d'une session opencode, les skills apparaissent dans la liste des skills disponibles. Si l'un n'apparaît pas :

1. Vérifier que le fichier s'appelle bien `SKILL.md` (majuscules).
2. Vérifier que le frontmatter contient `name` et `description`.
3. Vérifier que les noms sont uniques entre toutes les sources de skills.
4. Vérifier les permissions `skill` dans `opencode.json` (un `deny` masque le skill).

## Utilisation

Les skills se déclenchent automatiquement selon la tâche, ou explicitement :

```
Scaffold une infra AgenticOS avec un agent S1 et un agent d'actions externes
Ajoute la mémoire inter-runs avec rétention à 30 jours
Déploie la passerelle LiteLLM avec fallbacks et budgets par tenant
Audite mon infra AgenticOS
```

Enchaînement type : `agenticos-scaffold` pour poser la structure → `agenticos-securite` et `agenticos-memoire` pour les briques → `agenticos-deploiement` pour le socle → `agenticos-create-agent` pour chaque nouvel agent → `agenticos-eval` avant tout changement → `agenticos-migration` pour tout déplacement de composant → `agenticos-audit` pour vérifier que le déclaré = l'exécuté. Si Hermes Agent (NousResearch) sert d'assistant opérateur, `agenticos-hermes-integration` encadre sa coexistence avec le socle.
