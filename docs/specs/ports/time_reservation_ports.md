# Spec: Time reservation ports (minimal)

## Purpose
Define deterministic application ports for creating and querying reservations without infrastructure coupling.

## Responsibilities
- Create and update reservation records.
- Expose read-only access to reservation data within organization scope.
- Keep reservation data shapes stable for downstream engines.

## Inputs / Outputs (data shapes, not code)
### CreateReservation
Input
- organization_id
- resource_id (optional)
- starts_at_utc
- ends_at_utc
- timezone
- economic_value

Output: Reservation
- id
- organization_id
- resource_id (optional)
- starts_at_utc
- ends_at_utc
- timezone
- economic_value
- status (draft, active, cancelled)

### UpdateReservation
Input
- reservation_id
- starts_at_utc (optional)
- ends_at_utc (optional)
- resource_id (optional)
- status (optional)

Output: Reservation
- id
- organization_id
- resource_id (optional)
- starts_at_utc
- ends_at_utc
- timezone
- economic_value
- status

### GetReservation
Input
- reservation_id

Output: Reservation
- id
- organization_id
- resource_id (optional)
- starts_at_utc
- ends_at_utc
- timezone
- economic_value
- status

### ListReservations
Input
- organization_id
- resource_id (optional)
- time_range (optional; start_utc, end_utc)

Output: Reservation[]
- id
- organization_id
- resource_id (optional)
- starts_at_utc
- ends_at_utc
- timezone
- economic_value
- status

## Invariants (referenced)
- starts_at_utc MUST be earlier than ends_at_utc.
- All reservations MUST be stored in UTC; timezone is metadata only.
- Reservation MUST be scoped to an organization.
- resource_id MAY be empty to represent unassigned work.
Reference: docs/specs/time_reservation_engine.md, docs/specs/18_invariants_minimal.md.

## Explicit NON-responsibilities
- No conflict detection or resolution.
- No recurrence rules, buffers, or travel time logic.
- No persistence or storage decisions.
- No API or transport protocol definitions.

## Traceability
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md (Time and reservation engine)
- Roadmap: docs/roadmap/roadmap_v1.md (Phase 2)
- Source spec: docs/specs/time_reservation_engine.md
