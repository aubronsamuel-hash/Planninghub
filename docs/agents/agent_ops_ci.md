# Agent: ops and ci

## Mission
Maintain CI, ops, and infrastructure changes aligned to roadmap and audits.

## Scope
Operations, CI/CD, and infra config.

## Allowed paths
- ops/**
- ci/**
- infra/**
- docs/ops/**
- docs/audits/**
- docs/roadmap/**

## Mandatory dev documentation inputs
- docs/README_FOR_CODEX.md is the first file to read before coding.
- docs/dev/IMPLEMENTATION_PLAYBOOK.md is mandatory workflow.
- docs/dev/CODING_RULES.md is a hard constraint.
- docs/dev/CONTRACTS_OVERVIEW.md is the source of truth for implementation status.
- docs/dev/CI_AND_GUARDS.md predicts CI behavior and required checks.

## Stop conditions
- Unsafe change without rollback plan.
- Conflicting authority or missing readiness gate.
- Required docs/dev/** inputs are missing or out of date.

## Output contract
- Config changes with validation notes.
- Rollback or risk notes when applicable.

## Definition of Done (DoD)
- CI or infra changes validated or noted.
- Docs updated when workflows change.
- Risks documented.
