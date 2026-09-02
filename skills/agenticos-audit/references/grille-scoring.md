# Grille de scoring — AgenticOS Audit

## Niveaux de criticité

| Niveau | Définition | Exemples AgenticOS | Délai cible |
|---|---|---|---|
| **P0 — Critique** | Fuite active, incident en attente, ou protection contournee en prod | Rôle par défaut fail-open ; secrets en clair (dépôt ou `aos_audit`) ; chemin d'exécution sans sandbox ni validation touchant des données S1 ; mot de passe console faible | Jour 0 — avant toute autre chose |
| **P1 — Majeur** | Écart déclaré/exécuté, risque élevé mais non actif | `routing-policies.yaml` jamais chargé ; `force_local` non enforcé ; `human_validation` contournable ; fallback `fast` absorbant le trafic ; mémoire > 80 % sans rétention ; exécutions zombies sans reaper | Semaine en cours |
| **P2 — Amélioration** | Robustesse, dette, bonnes pratiques | Tool calling natif vs parser ; dashboards manquants ; runbook incomplet ; ADR absents | Planifié |

## Règles de priorisation

1. **Exploitabilité d'abord** : un P0 se juge sur « est-ce que ça peut mal tourner demain ? », pas sur l'élégance.
2. **Coût nul ≠ priorité basse** : les fixes J0 ne coûtent rien et éliminent le pire — toujours en tête.
3. **Ordre des chantiers** : sécurité immédiate → honnêteté du système (le YAML dit la vérité) → unification des chemins → mémoire/état → gouvernance résiduelle. Justifier tout écart à cet ordre.
4. **Quick wins vs chantiers** : chaque recommandation porte un effort estimé (heures / jours) et sa classe (quick win / chantier).

## Format d'un finding

```
[P0] Titre court
  Constat        : ce qui est observé
  Preuve         : fichier:ligne, commande, log
  Risque         : conséquence concrète
  Recommandation : action précise
  Effort         : estimation honnête
```

## Score global (optionnel, si demandé)

- **Sécurité /25**, **Architecture /25**, **Fiabilité /25**, **Observabilité & gouvernance /25**
- Ne pas donner de score rassurant si des P0 existent : tout P0 plafonne la note à 40/100.
