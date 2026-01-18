# Spec: Conflict engine minimal

## Purpose
Define minimal conflict detection contracts for overlapping reservations.

## Scope
- Conflict detection within a single organization.
- Severity classification for detected conflicts.

## Non-scope
- Automatic resolution actions.
- External legal or compliance checks.
- Cross organization budget rules.

## Core concepts and glossary
- Conflict: a detected overlap or rule violation tied to a reservation.
- Severity: categorical priority assigned to a conflict.

## Data model (conceptual)
- Conflict
  - id
  - organization_id
  - reservation_id
  - resource_id (optional)
  - severity (critical, high, medium, low)
  - reason

## Commands and queries (ports)
- DetectConflicts(input: organization_id, reservation_id) -> Conflict[]
- ListConflicts(input: organization_id, reservation_id?) -> Conflict[]

## Invariants
- A conflict MUST reference a reservation in the same organization.
- Severity MUST be one of: critical, high, medium, low.
- Overlapping reservations for the same resource MUST emit at least one conflict.

## Error taxonomy
- NotFound: reservation does not exist.
- Forbidden: reservation not in caller organization.

## Open questions
- Should conflict reasons be enumerated or free text?
- Do we need a separate conflict status for acknowledgement?

## Traceability
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md (Conflict detection and resolution)
- Roadmap: docs/roadmap/roadmap_v1.md (Phase 1)
