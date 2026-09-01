# Services Externes

Skills pour services externes (Zabbix, Proxi, etc.) — inté «grations avec des systè««mes tiers.

## Skills Disponibles

| Skill | Version | External | Description |
|-------|---------|----------|-------------|
| [`zabbix-proxi-monitor`](./zabbix-proxi-monitor/SKILL.md) | 1.0.0 | Zabbix | Surveillance Proxi |

## À Venir (Phase 2)

- `grafana-dashboard-sync` — Sync dashboards Grafana
- `prometheus-alerts` — Gestion alertes Prometheus
- `vault-secrets-manager` — Gestion secrets HashiCorp Vault
- `kubernetes-health-check` — Health checks K8s

## Structure

Chaque skill externe suit le format standard :

```
zabbix-proxi-monitor/
├── SKILL.md
├── skill.yaml          (à«« venir)
├── tests/
└── evals/
```

Voir [`standards/skill-spec-v2.md`](../../standards/skill-spec-v2.md).
