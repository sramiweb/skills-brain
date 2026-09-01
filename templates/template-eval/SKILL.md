---
name: template-eval
description: Use this skill when the user wants to evaluate the quality of any agent/service. Triggers on "evaluate", "eval agent", "quality check". Do NOT use for security or deployment tasks.
license: MIT
compatibility: opencode, claude-code
metadata:
  author: S R
  version: "1.0.0"
  category: templates
---

# Template: Evaluation

## Purpose

Evaluates the quality of an agent/service (tests, metrics, performance).

## Workflow

1. Run test suite
2. Collect metrics (latency, errors, throughput)
3. Compare against thresholds
4. Report PASS/FAIL with details

## Examples

### Happy path
- **Input:** "Evaluate `zabbix-proxi-monitor`"
- **Expected:** Tests run, metrics collected
- **Actual:** All PASS
- **Status:** PASS · Level: L1

## References

- `agenticos-agent-audit`
