# Spec: Invariants (minimal)

## Purpose
List cross-spec invariants and minimal edge cases needed to implement core entities without ambiguity.

## Non-goals
- Full validation rules for advanced workflows.
- Business-specific policy enforcement.

## Invariants
- All org-scoped entities must carry organization_id (except User).
- User is global; Membership ties User to Organization.
- Reservation interval invariant: starts_at_utc < ends_at_utc, stored UTC, timezone metadata.
- Shift references exactly one Reservation.
- Conflicts are detected by conflict engine; reservation engine does not block overlaps by itself.

## Error and edge cases
- Missing organization_id is invalid for org-scoped entities.
- Zero-length reservation interval is invalid.
- Duplicate membership for the same user and organization is invalid.

## References
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md
- Roadmap: docs/roadmap/roadmap_v1.md (Foundation steps 1-2)
- Core domain: docs/specs/core_domain_model.md
- Time reservation: docs/specs/time_reservation_engine.md
- IAM: docs/specs/iam_minimal.md
- Conflict engine: docs/specs/conflict_engine_minimal.md
