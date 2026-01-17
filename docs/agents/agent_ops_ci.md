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

## Stop conditions
- Unsafe change without rollback plan.
- Conflicting authority or missing readiness gate.

## Output contract
- Config changes with validation notes.
- Rollback or risk notes when applicable.

## Definition of Done (DoD)
- CI or infra changes validated or noted.
- Docs updated when workflows change.
- Risks documented.
