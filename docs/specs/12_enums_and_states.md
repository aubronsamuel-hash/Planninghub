# Spec: Enums and states (minimal)

## Purpose
Define canonical enums used across foundation specs to keep state vocabulary consistent.

## Non-goals
- Workflow transitions or lifecycle automation.
- Additional roles, severities, or resource types beyond foundation scope.

## Canonical enums
- Membership role: owner, admin, member
- Resource type: human, asset, service
- Shift status: proposed, accepted, confirmed, in_progress, completed, validated, closed
- Reservation status: draft, active, cancelled
- Conflict severity: critical, high, medium, low

## Invariants
- Each enum value must be one of the allowed ASCII strings listed above.
- Specs referencing these enums must use the canonical values without aliases.

## References
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md
- Roadmap: docs/roadmap/roadmap_v1.md (Foundation steps 1-2)
- Core domain: docs/specs/core_domain_model.md
- Time reservation: docs/specs/time_reservation_engine.md
- IAM: docs/specs/iam_minimal.md
- Conflict engine: docs/specs/conflict_engine_minimal.md
