---
name: "Agenticos Migration Runner"
version: "1.0.0"
status: "active"
---

# Agenticos Migration Runner

Run database and service migrations safely with rollback capability.

## Purpose

This skill executes database schema migrations and data migrations with built-in safety checks and rollback mechanisms.

## Workflow

1. **Pre-flight checks**: Validate migration scripts and backup state
2. **Execution**: Run migrations in transactional batches
3. **Verification**: Confirm migration success and data integrity
4. **Rollback (if needed)**: Revert migrations on failure

## Inputs

- `migration_scripts`: List of migration script paths
- `target_environment`: Target environment (dev, staging, prod)
- `rollback_enabled`: Enable automatic rollback on failure (default: true)

## Outputs

- `migration_report`: JSON report with execution details
- `rollback_script`: Generated rollback script
- `status`: Success/failure status

## Examples

```yaml
skill: agenticos/migration-runner
inputs:
  migration_scripts:
    - "migrations/001_add_users.sql"
    - "migrations/002_add_indexes.sql"
  target_environment: "prod"
  rollback_enabled: true
```

## Quality Gates

- **Q0**: Structure ✓
- **Q1**: YAML Syntax ✓
- **Q2**: Schema Compliance ✓
- **Q3**: Scenarios (TODO)
- **Q4**: Golden Tasks (TODO)
- **Q5**: Security Scan ✓

## Changelog

- **1.0.0** (2026-09-01): Initial v2 release
