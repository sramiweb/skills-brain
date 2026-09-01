---
name: zabbix-proxi-monitor
description: Use this skill when the user wants to monitor Proxi services via Zabbix. Triggers on "monitor proxi", "zabbix check proxi", "proxi status". External service integration.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: services
  external: zabbix
---

# Skill: Zabbix Proxi Monitor

## Purpose

Surveille les services Proxi via Zabbix : santé des hosts, métriques, alertes.

## Workflow

1. **Connecter Zabbix API** : Auth avec token/API key.
2. **Ré««cupé««rer hosts Proxi** : Filtrer par tag/group `proxi`.
3. **Collecter métriques** : CPU, mé «moire, disk, network, uptime.
4. **Vé««rifier alertes** : Lire triggers actifs (WARNING/CRITICAL).
5. **Rapport** : Status par host + métriques + alertes.

## Examples

### Happy path
- **Input** : "Monitor Proxi services via Zabbix"
- **Expected** : Tous hosts OK, 0 alertes
- **Actual** : 5 hosts UP, 0 CRITICAL, 2 WARNING
- **Status** : PASS · Level: L1

### Alerte CRITICAL
- **Input** : "Check Proxi status on Zabbix"
- **Expected** : Dé «tecter host down
- **Actual** : 1 host DOWN (proxi-api-03), 1 CRITICAL
- **Status** : FAIL · Level: L1

## References

- Zabbix API : https://www.zabbix.com/documentation/current/en/manual/api
- Proxi docs : https://docs.proxi.io/
