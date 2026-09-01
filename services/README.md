# Services Externes

Skills pour services externes (Zabbix, Proxi, etc.) — inté «grations avec des systè««mes tiers.

## Skills à Créer (Phase 2)

| Skill | Description | Triggers |
|-------|-------------|----------|
| `zabbix-proxi-monitor` | Surveillance Proxi via Zabbix | `monitor proxi`, `zabbix check` |
| `grafana-dashboard-sync` | Sync dashboards Grafana | `sync grafana`, `update dashboard` |
| `prometheus-alerts` | Gestion alertes Prometheus | `prometheus alerts`, `add alert` |
| `vault-secrets-manager` | Gestion secrets HashiCorp Vault | `vault secrets`, `rotate secret` |
| `kubernetes-health-check` | Health checks K8s | `k8s health`, `check pods` |

## Structure

Chaque skill suit le format standard :

```
services/
├── README.md
├── zabbix-proxi-monitor/
│   └── SKILL.md
├── grafana-dashboard-sync/
│   └── SKILL.md
└── ...
```

## Prochaines É «tapes

1. Créer `zabbix-proxi-monitor` (1er skill externe)
2. Ajouter 4-9 autres skills
3. Inté««gration CI/CD

Voir [`SPECIFICATION.md`](../SPECIFICATION.md) pour les standards.
