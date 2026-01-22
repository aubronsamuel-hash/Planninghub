# Agent: backend

## Mission
Implement backend code changes that follow approved specs and roadmap steps.

## Scope
Backend code and supporting docs for backend execution.

## Allowed paths
- planninghub/**
- docs/specs/**
- docs/roadmap/**
- docs/audits/**

## Mandatory dev documentation inputs
- docs/README_FOR_CODEX.md is the first file to read before coding.
- docs/dev/IMPLEMENTATION_PLAYBOOK.md is mandatory workflow.
- docs/dev/CODING_RULES.md is a hard constraint.
- docs/dev/CONTRACTS_OVERVIEW.md is the source of truth for implementation status.
- docs/dev/CI_AND_GUARDS.md predicts CI behavior and required checks.

## Stop conditions
- No approved NEXT STEP in implementation_readiness.md.
- Spec ambiguity or missing invariants.
- Required docs/dev/** inputs are missing or out of date.

## Output contract
- Code changes aligned to specs.
- Tests or validation recorded.
- Notes on risks or follow ups.

## Definition of Done (DoD)
- Code matches the referenced spec.
- Validation recorded or explicitly skipped with reason.
- Docs updated if behavior changes.
