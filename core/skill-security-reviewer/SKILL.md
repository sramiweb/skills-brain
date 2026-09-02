---
name: skill-security-reviewer
description: Independently review a Skill package for security, permission, side-effect and supply-chain risks before promotion.
license: MIT
compatibility: skills-brain, agenticos
metadata:
  author: sramiweb
  version: "1.0.0"
  category: core
---

# Skill Security Reviewer

## Purpose

Perform an independent adversarial security review of a Skill candidate or new Skill version. The reviewer evaluates the Skill's declared behavior and package contents; it never grants runtime permissions and never activates the Skill.

## Inputs

- `SKILL.md`;
- `skill.yaml`;
- package hash and provenance;
- tests/evals when present;
- dependency and compatibility metadata;
- relevant security policy or runtime constraints supplied by the caller.

## Workflow

1. Confirm the Skill identity, version, source and package integrity.
2. Compare documented behavior with declared `risk`, `side_effects` and `security` fields.
3. Review logical tool capabilities for least privilege.
4. Check whether filesystem, network, shell or destructive behavior is under-declared.
5. Review data-class compatibility and potential sensitive-data exposure.
6. Inspect dependencies, scripts, resources and references for unexpected execution or supply-chain behavior.
7. Check whether the Skill could encourage bypassing approvals, tenant isolation, sandboxing or runtime policy.
8. Review negative/security test coverage and Q4/Q5 evidence appropriate to the risk level.
9. Identify assumptions and missing evidence.
10. Return a structured verdict and blocking findings.

## Security verdicts

- `approve`: no blocking security finding with sufficient evidence;
- `approve_with_conditions`: bounded remediation or additional evidence required before activation;
- `retest`: security behavior cannot yet be established reliably;
- `reject`: design violates governance/security requirements;
- `quarantine`: known or suspected behavior creates an immediate safety/supply-chain concern.

## Blocking examples

- undeclared `shell.execute` behavior;
- network outbound behavior with no logical requirement;
- a destructive operation declared as low risk;
- a package containing unexpected executable resources;
- instructions that tell an agent to bypass human approval;
- a Skill that embeds credentials, tenant secrets or private infrastructure details;
- stale or missing high-risk regression evidence.

## Rules

- Treat permission widening as a blocker, not a scoring penalty.
- Do not infer safety from the absence of observed incidents.
- Preserve dissenting high-severity findings even if other reviewers approve.
- Distinguish canonical Skill requirements from runtime-specific permissions.
- Never modify the reviewed Skill as part of the review.

## Output

Return:

- verdict;
- severity-ranked findings;
- evidence references;
- undeclared or excessive capabilities;
- data/security concerns;
- required remediation;
- additional tests/evidence required;
- quarantine recommendation when applicable.
