# Skills Brain v2.1 — Spécification

**Version :** 2.1  
**Statut :** spécification normative  
**Dernière mise à jour :** 2026-09-02

## 1. Vision

Skills Brain est un **Skill Intelligence & Governance Plane** open source pour définir, versionner, découvrir, évaluer, sécuriser et faire évoluer des compétences réutilisables par des agents IA.

Un Skill décrit **comment réaliser une capacité**. Il ne s'accorde jamais lui-même des permissions runtime.

```text
Skill = HOW to do something
Tool  = WITH WHAT to act
```

## 2. Positionnement

Skills Brain reste indépendant du runtime. Il peut être consommé par AgenticOS ou adapté à d'autres environnements.

```text
Skills Brain = Skills canoniques, capabilities, gouvernance, évaluation, protocoles
AgenticOS    = orchestration, bindings locaux, tenants, policies, approvals, exécution
Hermes       = runtime cognitif / raisonnement agentique
MCP          = outils et actions autorisés
LiteLLM      = routage des modèles
```

Règle fondamentale :

```text
Skills Brain propose la connaissance.
AgenticOS établit la confiance et les permissions.
Hermes applique la compétence.
MCP réalise les actions autorisées.
```

## 3. Architecture du dépôt

```text
skills-brain/
├── README.md
├── SPECIFICATION.md
├── standards/          # Règles normatives
├── schemas/            # Contrats machine JSON Schema
├── core/               # Meta-Skills de gouvernance
├── skills/             # Packages de Skills canoniques
├── protocols/          # Protocoles de débat et décision
├── catalog/            # Index générés
├── adapters/           # Contrats d'intégration runtime
├── tooling/            # Validation, évaluation, catalogue, résolution, intégrité
├── examples/           # Requêtes et contrats d'exemple
├── tests/              # Tests du repository/tooling
└── .github/workflows/  # CI
```

Le seul emplacement canonique des packages de Skills est `skills/`. Les standards ne doivent jamais contenir de copies exécutables de Skills.

## 4. Package Skill v2.1

Un Skill canonique contient au minimum :

```text
<skill>/
├── SKILL.md
└── skill.yaml
```

Il peut également contenir :

```text
README.md
CHANGELOG.md
tests/
evals/
references/
resources/
scripts/
fixtures/
```

`SKILL.md` contient les instructions portables destinées au raisonnement. `skill.yaml` contient le contrat machine de gouvernance.

Tous les nouveaux manifests utilisent :

```yaml
schema_version: "2.1"
```

Le schéma strict de référence est `schemas/skill.schema.json` avec `additionalProperties: false`.

Le schéma `schemas/skill-v2.0.schema.json` existe uniquement pour compatibilité/migration de manifests historiques ; il ne doit pas être utilisé pour créer de nouveaux Skills.

## 5. Identité et compatibilité

Chaque Skill possède un `id` canonique stable et un `version` SemVer.

Les anciennes identités peuvent être conservées via `aliases` afin de migrer sans maintenir plusieurs copies physiques du même Skill.

Un Skill peut déclarer une compatibilité runtime, par exemple :

```yaml
compatibility:
  agenticos: ">=3.1"
```

La compatibilité déclarée n'accorde aucune permission.

## 6. Capability Ontology

Les Skills déclarent des **capabilities logiques**, jamais des outils vendor-specific comme vérité canonique.

Exemples :

```text
product.discover
sales.lead.qualify
engineering.code.review
sre.application.health
database.postgres.diagnose
```

L'ontologie machine est définie dans `standards/capabilities.yaml` et validée par `schemas/capability.schema.json`.

Les besoins d'accès sont déclarés séparément comme `tool_capabilities` :

```text
filesystem.read
logs.read
monitoring.read
network.outbound
```

AgenticOS mappe ensuite ces exigences logiques vers ses connecteurs et outils MCP réels.

## 7. Sécurité et autorité

Un Skill déclare :

- niveau de risque ;
- classe de side effect ;
- contraintes réseau ;
- accès filesystem ;
- besoin shell ;
- opérations destructives ;
- classes de données autorisées lorsque nécessaire.

Classes de side effects :

```text
none
local
reversible
external
destructive
```

Le runtime consommateur doit être plus restrictif ou égal aux besoins du Skill, jamais plus permissif par simple demande du Skill.

Pour AgenticOS :

```text
effective permissions = intersection(
  Skill requirements,
  AgenticOS binding,
  tenant policy,
  MCP/tool policy
)
```

Toute incompatibilité doit être fail-closed.

## 8. Lifecycle

Lifecycle canonique :

```text
DRAFT
  -> REVIEW
  -> CANDIDATE
  -> APPROVED
  -> ACTIVE
  -> DEPRECATED
  -> RETIRED

QUARANTINED = état de sécurité exceptionnel
```

Un runtime peut gérer un lifecycle de déploiement distinct : disponible, téléchargé, installé, activé, désactivé, quarantined.

Un Skill `candidate` n'est pas automatiquement production-ready.

## 9. Quality Gates Q0–Q5

Les définitions canoniques sont :

| Gate | Signification |
|---|---|
| Q0 | Schema |
| Q1 | Static quality |
| Q2 | Scenario tests |
| Q3 | Security / sandbox |
| Q4 | Golden Task execution |
| Q5 | Regression evidence |

`tooling/evaluator.py`, `tooling/eval_harness.py`, la CI et la documentation doivent utiliser ces mêmes définitions.

Q4 et Q5 ne peuvent pas être déclarés PASS par simple présence d'un fichier de définition ou par un résultat auto-déclaré. Ils nécessitent une chaîne de preuve :

```text
PREPARE
  -> EXECUTION EXTERNE
  -> VERIFICATION INDEPENDANTE
  -> FINALIZE
  -> RE-VALIDATION EVALUATOR
```

`tooling/eval_harness.py prepare` lie un run à :

- l'ID et la version du Skill ;
- son `package_sha256` ;
- le hash exact de `golden.yaml` ou `regression.yaml` ;
- les IDs et critères/checks exacts ;
- le commit source lorsqu'il est disponible.

Le runner externe produit une observation conforme à `schemas/eval-runner-results.schema.json`. Un vérificateur distinct produit une vérification conforme à `schemas/eval-verification.schema.json`.

Le harness refuse la finalisation lorsque :

- le package a changé depuis `prepare` ;
- la définition d'évaluation a changé ;
- les IDs ne couvrent pas exactement la requête ;
- un critère ou comportement interdit n'est pas vérifié ;
- runner et verifier utilisent la même identité ;
- `independent` n'est pas vrai.

Le résultat canonique `*-results.json` est conforme à `schemas/eval-results.schema.json` v2.0. `tooling/evaluator.py` recalcule ensuite package hash, definition hash et couverture des IDs avant d'accepter Q4/Q5.

Une preuve Q4/Q5 devient donc automatiquement stale dès que le Skill ou sa définition d'évaluation change.

La CI bloque un Skill `approved` ou `active` qui ne satisfait pas les gates exigés.

La norme complète est `standards/evaluation.md`.

## 10. Intégrité Supply Chain

Skills Brain définit trois hashes :

```text
skill_sha256
manifest_sha256
package_sha256
```

La norme détaillée est `standards/integrity.md`.

`package_sha256` couvre par défaut **tous les fichiers du package**, sauf exclusions explicites documentées. Cela évite qu'un nouveau répertoire `scripts/`, `resources` ou `assets/` échappe silencieusement au contrôle d'intégrité.

Le champ `integrity` éventuel de `skill.yaml` est exclu du hash canonique pour éviter l'auto-référence. Les fichiers générés `*-results.json` sont exclus du package hash : une preuve d'évaluation ne doit pas changer l'identité du package évalué.

Un runtime doit pinner :

```text
source commit/tag résolu
+
package_sha256
```

Un mismatch d'intégrité doit bloquer l'installation/l'exécution.

## 11. AgenticOS Adapter Contract

`adapters/agenticos/` exporte un contrat de gouvernance conforme à `schemas/agenticos-export.schema.json`.

L'export contient :

- identité et version du Skill ;
- source repository/commit/path ;
- capabilities ;
- exigences logiques d'outils ;
- risque, side effects, sécurité et évaluation ;
- hashes d'intégrité.

Il ne contient et ne doit jamais accorder :

- tenant ;
- agent runtime ;
- connecteur MCP ;
- outil MCP concret ;
- credentials ;
- mounts ;
- network profile ;
- approbation ;
- permission d'exécution.

Ces éléments restent exclusivement locaux à AgenticOS.

## 12. Deliberation

Skills Brain fournit des protocoles de débat réutilisables :

- `strategic-debate-v1` ;
- `technical-debate-v1` ;
- `operational-debate-v1`.

Principes :

- premier tour indépendant ;
- arguments fondés sur preuves ;
- cross-examination ;
- positions révisées ;
- dissent conservé ;
- jugement indépendant ;
- security veto ;
- coût/rounds bornés ;
- validation humaine lorsque la policy runtime l'exige.

La délibération de Skills Brain concerne la qualité/sélection/promotion des Skills. Une délibération AgenticOS concerne l'autorisation d'une action réelle dans un contexte runtime. Les deux responsabilités ne doivent pas être confondues.

## 13. Learning

Skills Brain distingue mémoire et apprentissage :

```text
SIGNAL
  -> PATTERN
  -> HYPOTHESIS
  -> VERIFIED LEARNING
  -> OPERATIONALIZED KNOWLEDGE
```

Le cycle d'amélioration est :

```text
Outcome
  -> Retrospective
  -> Improvement Proposal
  -> Tests
  -> Evaluation
  -> Review / Debate
  -> Approval
  -> Skill vNext
```

Aucun feedback runtime ne modifie automatiquement un Skill production.

## 14. Meta-Skills Core

Composants actuellement présents :

- `skill-creator` ;
- `skill-reviewer` ;
- `skill-security-reviewer` ;
- `skill-evaluator` ;
- `skill-resolver` ;
- `skill-composer` ;
- `skill-deliberator` ;
- `skill-retrospective`.

Responsabilités :

```text
creator             -> crée un candidat
reviewer            -> revue générale indépendante
security-reviewer   -> revue sécurité/supply-chain/least-privilege
 evaluator           -> Q0-Q5 et preuves
resolver            -> candidats éligibles, authorization=not_granted
composer            -> plan multi-Skill minimal, authorization=not_granted
deliberator          -> débat gouverné
retrospective       -> apprentissage à partir d'outcomes
```

La composition ne peut utiliser que des Skills déjà éligibles et ne transforme jamais l'union de leurs requirements en permissions runtime.

## 15. Catalogue et résolution

`tooling/catalog.py` génère :

```text
catalog/index.json
catalog/capabilities.json
catalog/dependencies.json
catalog/compatibility.json
```

Le catalogue est dérivé des manifests canoniques. Il ne devient pas une seconde source de vérité.

`tooling/resolver.py` filtre d'abord l'éligibilité : ontology, capability overlap, lifecycle, risk ceiling, tools, data class et compatibilité. Le ranking n'intervient qu'après ces filtres et retourne toujours :

```json
{"authorization": "not_granted"}
```

La norme est `standards/resolution.md`.

## 16. Klerbot comme Golden Tenant

Klerbot sert de premier cas end-to-end pour valider la séparation entre Skills génériques et contexte tenant.

Les méthodes réutilisables restent dans leurs domaines génériques :

```text
market/
product/
customer/
revenue/
growth/
content/
sales/
engineering/
sre/
databases/
```

`skills/klerbot/` contient uniquement du contexte ou des conventions Klerbot qui ne sont pas généralisables.

## 17. Validation et CI

Commandes de référence :

```bash
pip install -r requirements-dev.txt
python tooling/validate.py --all
pytest -q
python tooling/evaluator.py
python tooling/catalog.py
python tooling/resolver.py examples/resolution-request.json
python tooling/eval_harness.py --help
```

La CI vérifie notamment :

- UTF-8 ;
- schema v2.1 ;
- capability ontology ;
- syntaxe Python ;
- tests ;
- calcul d'intégrité de tous les packages ;
- evidence Q0–Q5 ;
- interdiction de promotion sans preuves ;
- génération du catalogue.

## 18. Anti-patterns interdits

Ne pas :

- charger `main` dynamiquement pendant une mission ;
- laisser un worker installer un Skill ;
- exécuter automatiquement du code upstream pour établir la confiance ;
- accorder les outils demandés par un Skill sans policy locale ;
- confondre Skill, Agent et Tool ;
- maintenir plusieurs copies physiques du même Skill ;
- considérer un score de qualité comme une autorisation ;
- fabriquer des résultats Golden/Regression ;
- accepter un résultat Q4/Q5 stale après modification du package ou de sa définition ;
- accepter l'auto-vérification runner=verifier ;
- permettre à un Skill de réduire son niveau de risque ;
- auto-modifier un Skill de production depuis le feedback runtime.

## 19. Roadmap

| Phase | Objectif | État v2.1 |
|---|---|---|
| P0 | Structure canonique + nettoyage des doublons | Réalisé |
| P1 | Schema strict + CI + ontology | Réalisé |
| P2 | Q0–Q5 evidence-based + Golden/Regression harness | Harness implémenté ; qualification avec runners runtime externes en cours |
| P3 | Intégrité supply-chain + adapter AgenticOS | Réalisé |
| P4 | Catalogue + resolver + composition | Resolver v1 et guidance composer implémentés ; orchestration multi-Skill runtime à venir |
| P5 | Learning / retrospective | Fondation réalisée |
| P6 | Deliberation | Fondation réalisée |
| P7 | Reputation / adapters supplémentaires / composition avancée | Planifié |

## 20. Références normatives

- `standards/skill-spec-v2.md`
- `standards/capabilities.yaml`
- `standards/evaluation.md`
- `standards/integrity.md`
- `standards/resolution.md`
- `standards/deliberation.md`
- `standards/learning.md`
- `schemas/skill.schema.json`
- `schemas/eval-run.schema.json`
- `schemas/eval-runner-results.schema.json`
- `schemas/eval-verification.schema.json`
- `schemas/eval-results.schema.json`
- `schemas/agenticos-export.schema.json`
