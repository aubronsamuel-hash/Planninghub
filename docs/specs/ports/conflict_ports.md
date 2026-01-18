# Spec: Conflict ports (minimal)

## Purpose
Define deterministic ports for conflict detection outputs without embedding resolution logic.

## Responsibilities
- Accept conflict detection requests scoped to an organization.
- Return conflict records with severity and reason.
- Provide query access to stored conflict records.

## Inputs / Outputs (data shapes, not code)
### DetectConflicts
Input
- organization_id
- reservation_id

Output: Conflict[]
- id
- organization_id
- reservation_id
- resource_id (optional)
- severity (critical, high, medium, low)
- reason

### ListConflicts
Input
- organization_id
- reservation_id (optional)

Output: Conflict[]
- id
- organization_id
- reservation_id
- resource_id (optional)
- severity
- reason

## Invariants (referenced)
- A conflict MUST reference a reservation in the same organization.
- Severity MUST be one of: critical, high, medium, low.
- Overlapping reservations for the same resource MUST emit at least one conflict.
Reference: docs/specs/conflict_engine_minimal.md, docs/specs/18_invariants_minimal.md.

## Explicit NON-responsibilities
- No automatic resolution actions.
- No external compliance checks.
- No persistence or storage decisions.
- No API or transport protocol definitions.

## Traceability
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md (Conflict detection and resolution)
- Roadmap: docs/roadmap/roadmap_v1.md (Phase 2)
- Source spec: docs/specs/conflict_engine_minimal.md
