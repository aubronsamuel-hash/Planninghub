# Agent: data model

## Mission
Define and implement data models and schemas that support core domain objects.

## Scope
Data model documentation and schema changes.

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
- Spec lacks invariants or conflict rules.
- Required docs/dev/** inputs are missing or out of date.

## Output contract
- Data model updates aligned to specs.
- Migration or schema notes when needed.

## Definition of Done (DoD)
- Models match spec definitions.
- Invariants documented or enforced.
- Validation recorded or reasoned skip.
