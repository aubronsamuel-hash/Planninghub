# Spec: Time reservation engine (minimal)

## Purpose
Define the minimal reservation primitives that represent time as the source of truth.

## Scope
- Reservation interval and assignment to organization and optional resource.
- Status lifecycle for a reservation record.

## Non-scope
- Recurrence rules and exceptions.
- Travel time, buffers, or geo logic.
- Cross organization conflicts.

## Core concepts and glossary
- Reservation interval: a time window with start and end in UTC.
- Resource: a person or asset that can be assigned to a reservation.
- Economic value: a numeric value attached to the reservation for later finance logic.

## Data model (conceptual)
- Reservation
  - id
  - organization_id
  - resource_id (optional)
  - starts_at_utc
  - ends_at_utc
  - timezone
  - economic_value
  - status (draft, active, cancelled)

## Commands and queries (ports)
- CreateReservation(input: organization_id, resource_id?, starts_at_utc, ends_at_utc, timezone, economic_value) -> Reservation
- UpdateReservation(input: reservation_id, starts_at_utc?, ends_at_utc?, resource_id?, status?) -> Reservation
- GetReservation(input: reservation_id) -> Reservation
- ListReservations(input: organization_id, resource_id?, time_range?) -> Reservation[]

## Invariants
- starts_at_utc MUST be earlier than ends_at_utc.
- All reservations MUST be stored in UTC; timezone is metadata only.
- Reservation MUST be scoped to an organization.
- resource_id MAY be empty to represent unassigned work.

## Error taxonomy
- InvalidInterval: start is not earlier than end.
- NotFound: reservation does not exist.
- Forbidden: reservation not in caller organization.

## Open questions
- Do we need a draft to active transition guard beyond status values?
- Should economic_value be optional for the skeleton?

## Traceability
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md (Time and reservation engine)
- Roadmap: docs/roadmap/roadmap_v1.md (Phase 1)
