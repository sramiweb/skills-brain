# Format du rapport d'audit — AgenticOS

Produire le rapport en français, en Markdown, dans cet ordre :

## 1. Synthèse exécutive
- 3–5 phrases : état général, nombre de P0/P1/P2, risque dominant.
- Verdict direct (ex. « exploitable en l'état pour de la démo, pas pour de la prod S1 »).

## 2. Cartographie de l'existant
- Composants identifiés + **chemins d'exécution** (schéma texte/ASCII).
- Écarts déclaré vs exécuté repérés.

## 3. Autonomie réelle des agents — grille des 9 maillons
- Pour chaque agent de l'échantillon tracé (≥ 3 profils, dont un S1 et un à action externe) : tableau des 9 maillons (déclaration → planification → décision → appel outils → observation → mémoire → coordination → reprise → amélioration) notés présent / partiel / absent + preuve.
- Schéma de la boucle réellement observée, maillons contournés mis en évidence.
- Verdict par agent : autonomie démontrée ou non (une chaîne vaut son maillon le plus faible).

## 4. Findings P0 — Jour 0
Tableau : # | Action | Preuve | Effort. Ces items ne coûtent rien et précèdent tout le reste.

## 5. Findings détaillés
Groupés par axe (Sécurité / Architecture / Mémoire / Observabilité / Conformité), format `[Pn] Titre` (cf. `grille-scoring.md`). Chaque finding cite sa preuve.

## 6. Plan d'action ordonné
```
JOUR 0 (sécurité immédiate)
  → PHASE 1 (honnêteté : le déclaré dit la vérité)
  → PHASE 2 (unification des chemins)
  → PHASE 3 (mémoire et état)
  → PHASE 4 (gouvernance résiduelle)
```
Chaque item du plan se termine par une **preuve de fin** vérifiable (critère d'acceptation exécutable, pas « vérifier que… »).

## 7. Informations manquantes
Liste des points impossibles à auditer faute d'accès/données + ce qu'il faudrait fournir.

## Règles de rédaction
- Aucune recommandation sans preuve ni effort estimé.
- Jamais de big bang : les migrations se font item par item avec double-run de validation.
- Rappeler les règles transversales si un plan de remédiation est proposé : backup avant toute migration de données ; tests existants verts après chaque phase ; journal de refonte (`refonte-log.md`) ; en cas d'échec, diagnostiquer et proposer 2 options — pas de contournement silencieux.
