# Spec: Time reservation engine (minimal)

## Purpose
Define the minimal reservation primitives that represent time as the source of truth.

## Non-goals
- Recurrence rules and exceptions.
- Travel time, buffers, or geo logic.
- Multi org conflicts.

## Data model (minimal)
- Reservation
  - id
  - organization_id
  - resource_id (optional for unassigned reservations)
  - starts_at_utc
  - ends_at_utc
  - timezone
  - economic_value
  - status (draft, active, cancelled)

## Invariants
- starts_at_utc < ends_at_utc.
- All reservations are stored in UTC; timezone is metadata.
- Reservation can be unassigned (resource_id null) but must be scoped to an organization.

## Error and edge cases
- Overlapping reservations for the same resource should be flagged by conflict engine, not blocked here.
- Zero length intervals are invalid.

## References
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md
- Roadmap: docs/roadmap/roadmap_v1.md (Foundation step 1)
