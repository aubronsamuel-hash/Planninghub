# Spec: Persistence adapters (minimal)

## Purpose
Define adapter boundaries for storing and retrieving core domain records without selecting a database or schema.

## Responsibilities
- Persist and retrieve core domain entities for application ports.
- Preserve invariants defined in domain specs when writing or updating records.
- Provide deterministic read behavior for the application core.

## Inputs / Outputs (data shapes, not code)
Persistence adapters handle the following shapes as defined in existing specs:
- User, Organization, Membership (docs/specs/iam_minimal.md)
- Reservation (docs/specs/time_reservation_engine.md)
- Conflict (docs/specs/conflict_engine_minimal.md)
- Project, Site, Mission, Resource, Shift (docs/specs/core_domain_model.md)

## Invariants (referenced)
- Org-scoped entities MUST carry organization_id.
- Reservation interval invariant: starts_at_utc < ends_at_utc, stored UTC.
- Duplicate membership for the same user and organization is invalid.
- Shift references exactly one Reservation.
Reference: docs/specs/18_invariants_minimal.md.

## Explicit NON-responsibilities
- No database selection, schema design, or migrations.
- No caching strategy or replication policy.
- No API or transport protocol definitions.
- No conflict detection or scheduling logic.

## Traceability
- Roadmap: docs/roadmap/roadmap_v1.md (Phase 2 adapter boundaries, Phase 3 persistence skeleton)
- Source specs: docs/specs/iam_minimal.md, docs/specs/time_reservation_engine.md, docs/specs/conflict_engine_minimal.md, docs/specs/core_domain_model.md
