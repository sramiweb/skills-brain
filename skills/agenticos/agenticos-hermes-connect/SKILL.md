---
name: agenticos-hermes-connect
description: Integrate AgenticOS with Hermes as a governed cognitive runtime, using installed Skill snapshots and runtime policy.
license: MIT
compatibility: skills-brain-v2.1, agenticos-v3.1
metadata:
  author: sramiweb
  version: "1.0.0"
  category: agenticos
---

# AgenticOS Hermes Connect

## Purpose

Define how AgenticOS hands a governed mission context to a Hermes runtime worker. Hermes is treated as the reasoning/execution runtime, not as a standalone messaging protocol or source of permissions.

## Workflow

1. Resolve the AgenticOS mission, agent and selected Skill snapshot.
2. Verify the Skill is installed, checksummed and allowed for the tenant/runtime context.
3. Build minimal context: mission, selected SKILL.md, relevant references, memory and tool contracts.
4. Inject effective policy and allowed tool metadata into the worker context.
5. Start or invoke the Hermes runtime through an AgenticOS-authorized integration.
6. Allow Hermes to read only authorized Skills and call only authorized MCP tools.
7. Return execution observations, tool evidence and outcome metadata to AgenticOS.
8. AgenticOS performs final policy, verification, audit and learning steps.

## Inputs

- Mission context.
- Installed Skill identity/version/hash.
- Effective policy.
- Authorized tool contracts.

## Outputs

- Hermes execution result.
- Tool/observation evidence.
- Outcome metadata for AgenticOS evaluation.

## Guardrails

- Hermes never grants itself new permissions.
- Hermes never installs Skills directly from a floating Git branch.
- Runtime-specific endpoints, credentials and mounts belong to AgenticOS configuration, not this canonical Skill.
- AgenticOS remains the authority for approval, policy and audit.
