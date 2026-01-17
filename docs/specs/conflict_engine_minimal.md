# Spec: Conflict engine minimal

## Purpose
Define minimal conflict detection and priority rules.

## Non-goals
- Automatic resolution actions.
- External legal or compliance checks.
- Multi org budget rules.

## Data model (minimal)
- Conflict
  - id
  - organization_id
  - reservation_id
  - resource_id
  - severity (critical, high, medium, low)
  - reason

## Invariants
- A conflict references a single reservation and optional resource.
- Severity is one of: critical, high, medium, low.

## Error and edge cases
- Overlapping reservations for the same resource must produce at least high severity.
- Missing resource_id can still produce conflicts for org wide rules.

## References
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md
- Roadmap: docs/roadmap/roadmap_v1.md (Foundation step 2)
