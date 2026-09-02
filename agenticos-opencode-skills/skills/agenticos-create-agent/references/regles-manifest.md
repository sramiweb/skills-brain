# Règles manifest et prompt — création d'agent AgenticOS

## Sommaire
1. La règle d'alignement
2. Catalogues d'outils Prod / Dev
3. Outils supprimés et pièges
4. Contraintes force_local / fast
5. Checklist prompt

## 1. La règle d'alignement

> Tout outil cité dans le prompt d'un agent doit exister dans le **manifest** de l'agent **et** dans la **policy** du tenant. Sinon : refus serveur à l'exécution.

Un outil cité mais non déclaré produit des appels hallucinés, des échecs de parsing et des runs « techniques » qui polluent les métriques (`classify_run`). C'est la forme la plus courante du « YAML qui ment ».

## 2. Catalogues d'outils

Le template d'agent (`agents/TEMPLATE.md`) distingue deux catalogues :

| Catalogue | Contenu | Usage |
|---|---|---|
| **Prod (worker)** | Uniquement les outils du manifest de l'agent, filtrés par la policy | Exécution planifiée via orchestrateur |
| **Dev local (`run.py`)** | Liste limitée : `sql_query`, `sql_syndic`, `generate_pdf`, `send_email`, `send_message`, `poll_messages`, `spawn_sub_agent`, `write_file` | Tests explicites en local, jamais en prod |

Le prompt doit citer les outils Prod réellement utiles à l'agent — ni plus (fantômes), ni moins (capacité dégradée à documenter, ex. « template inatteignable : read_file refusé »).

## 3. Outils supprimés et pièges

- **`run_script` : supprimé** — ne jamais le citer, même en exemple.
- Outils fréquemment retirés car non implémentés côté worker : `write_file`, `send_message`, `poll_messages`, `read_file`, `list_files`, `sql_query` (hors dev). Vérifier le manifest **avant** de les promettre dans un prompt.
- Les connecteurs métier (`sql_syndic`, `debts`) peuvent être planifiés sans être implémentés : ne pas les citer tant que le connecteur n'est pas en prod.

## 4. Contraintes force_local / fast

- Les tenants `force_local` et les modèles `fast` **n'ont pas de tool calling fiable** : un agent à appels d'outils sur ces tenants restera bloqué par le routing (cohérence D1).
- Conséquence : sur ces tenants, n'écrire que des agents sans outils (analyse, rédaction), ou traiter le blocage comme une décision datée — jamais livrer un agent qui ne peut pas s'exécuter en prod.

## 5. Checklist prompt

- [ ] Chaque outil cité est dans le manifest de l'agent ET dans la policy du tenant.
- [ ] Aucun outil supprimé (`run_script`) ou non implémenté n'est cité.
- [ ] `data_class` et tenant cohérents avec la règle policy (S1 ⇒ `force_local`, `human_validation` si action externe).
- [ ] Bloc incidents : escalade vers mémoire + Telegram, pas d'outil de message non déclaré.
- [ ] Vocabulaire d'échec explicite (marqueurs `classify_run` : OK réel / technique / échec).
