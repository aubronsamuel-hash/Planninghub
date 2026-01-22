# Agent: docs governance

## Mission
Maintain governance docs, audits, and indexes so execution is safe and traceable.

## Scope
Documentation only. No code changes.

## Allowed paths
- docs/**
- AGENT.md
- README.md

## Mandatory dev documentation inputs
- docs/README_FOR_CODEX.md is the first file to read before documentation work.
- docs/dev/IMPLEMENTATION_PLAYBOOK.md governs any change workflow.
- docs/dev/CODING_RULES.md is mandatory for doc updates that affect developer rules.
- docs/dev/CONTRACTS_OVERVIEW.md is the status map for implementations.
- docs/dev/CI_AND_GUARDS.md informs validation and guard expectations.
- docs/dev/DOCUMENTATION_INVENTORY.md MUST be updated when new docs appear.
- docs/dev/INDEX.md MUST stay complete and linked.

## Stop conditions
- Conflicting authority or unclear source of truth.
- Missing index for a touched doc.
- Required docs/dev/** inputs are missing or out of date.

## Output contract
- Updated docs with indexes kept in sync.
- Audit or decision log updates when required.
- docs/dev/** remains coherent, indexed, and cross-linked.

## Definition of Done (DoD)
- All updated docs are indexed.
- Implementation_readiness.md includes NEXT STEP and DO NOT DO lines.
- Governance log updated with reasons.
