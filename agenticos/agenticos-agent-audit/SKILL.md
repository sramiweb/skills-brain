---
name: agenticos-agent-audit
description: Use this skill when the user wants to evaluate the quality of an agent/service on AgenticOS. Triggers on "evaluate agent agenticos", "audit agent", "agent quality check". Implements template-eval.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: agenticos
  template: template-eval
---

# Skill: AgenticOS Agent Audit

## Purpose

É«€value la qualit é d'un agent/service sur AgenticOS : tests, métriques (latence, erreurs, throughput), performance.

## Workflow

1. **Run test suite** : Tests unitaires, inté «gration, end-to-end.
2. **Collecter métriques** : Latence (p50/p95/p99), taux d'erreurs, throughput (req/s).
3. **Comparer thresholds** : Vérifier contre les SLA définis.
4. **Rapport** : PASS/FAIL avec dé «tails et recommandations.

## Examples

### Happy path
- **Input** : "Evaluate `zabbix-proxi-monitor` agent on agenticos"
- **Expected** : Tests OK, métriques dans les thresholds
- **Actual** : 100% tests PASS, latence p99 < 200ms
- **Status** : PASS · Level: L1

### É «chec (performance)
- **Input** : "Evaluate `api-service` agent on agenticos"
- **Expected** : Dé «tecter dégradation performance
- **Actual** : p99 latence = 500ms (threshold: 200ms)
- **Status** : FAIL · Level: L1

## References

- Template : [`template-eval`](../../templates/template-eval/SKILL.md)
- Doc AgenticOS : https://docs.agenticos.io/monitoring
