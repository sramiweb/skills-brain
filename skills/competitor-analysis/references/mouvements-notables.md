# Grille de détection des mouvements concurrentiels

## Types de mouvement

| Type | Indicateurs | Sévérité |
|---|---|---|
| **Lancement** | nouveau produit, nouvelle fonctionnalité, nouveau marché | forte si cible identique |
| **Repositionnement** | changement de cible, de pricing, de message | forte si cible identique |
| **Prix** | baisse/hausse, nouveau palier, gratuité | moyenne |
| **Expansion** | nouvelle géographie, nouveau segment | moyenne |
| **Signal de déclin** | fermeture, churn visible, départ fondateur | forte (alerte) |

## Règles

- Un mouvement n'est « notable » que s'il impacte une niche que nous visons ou
  couvrons (croiser avec la mémoire et le marché).
- Règle de preuve : au moins 1 source fiable (veille/scan/mémoire) ; sinon
  « non vérifié ».
- Alerte Telegram uniquement pour les mouvements de sévérité forte ; sinon
  le consigner dans l'analyse persistée.
