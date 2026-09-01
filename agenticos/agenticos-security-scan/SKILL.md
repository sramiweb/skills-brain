---
name: agenticos-security-scan
description: Use this skill when the user wants to audit security of a service on AgenticOS. Triggers on "security scan agenticos", "audit security agenticos", "agenticos security". Implements template-security-audit.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: agenticos
  template: template-security-audit
---

# Skill: AgenticOS Security Scan

## Purpose

Audit de sécurité complet pour un service hébergé«« sur AgenticOS : secrets, patterns dangereux, permissions, vulné««rabilité««s.

## Workflow

1. **Scan secrets** : Recherche credentials, API keys, tokens dans le code et configs.
2. **Patterns dangereux** : Dé «tecter `eval()`, `exec()`, shell injection, SQL injection.
3. **Permissions** : Valider RBAC, accès minimum, service accounts.
4. **Dé««pendances** : Scanner npm/pip/cargo pour vulné««rabilité««s connues (CVE).
5. **Rapport** : CRITICAL / WARNING / INFO avec recommandations.

## Examples

### Happy path
- **Input** : "Security scan `api-service` on agenticos"
- **Expected** : Scan complet, 0 critical
- **Actual** : 2 warnings (deps obsolè««tes), 0 critical
- **Status** : PASS · Level: L1

### Critical trouvé «
- **Input** : "Security scan `payment-service` on agenticos"
- **Expected** : Dé «tecter secrets exposé««s
- **Actual** : 1 CRITICAL (API key dans .env), 3 WARNING
- **Status** : FAIL · Level: L1

## References

- Template : [`template-security-audit`](../../templates/template-security-audit/SKILL.md)
- Doc AgenticOS : https://docs.agenticos.io/security
