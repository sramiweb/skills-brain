# Skills Templates

Generic reusable skill templates for common workflows.

## Available Templates

| Template | Description | Triggers |
|----------|-------------|----------|
| [`template-deployment`](./template-deployment/SKILL.md) | Deploy/rollback any service | `deploy`, `rollback`, `deployment template` |
| [`template-security-audit`](./template-security-audit/SKILL.md) | Security audit for any service | `security audit`, `audit security`, `security template` |
| [`template-migration`](./template-migration/SKILL.md) | Run database migrations | `run migration`, `migrate`, `migration template` |
| [`template-eval`](./template-eval/SKILL.md) | Evaluate agent/service quality | `evaluate`, `eval agent`, `quality check` |

## Usage

Each template provides:
- Standard workflow steps
- Example happy path
- References to AgenticOS-specific implementations

## Contributing

1. Copy a template as starting point
2. Adapt workflow to your needs
3. Add test cases
4. Update this README
