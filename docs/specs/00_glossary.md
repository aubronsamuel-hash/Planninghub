# Spec: Glossary

## Purpose
Define canonical terms used across foundation specs.

## Glossary
- Organization: An org-scoped tenant that owns projects, sites, missions, resources, shifts, reservations, and conflicts.
- User: A global identity that can belong to one or more organizations via memberships.
- Membership: The link between a user and an organization, including the role used for access scope.
- Project: An org-scoped container for missions and planning context.
- Site: An org-scoped location descriptor for missions and shifts.
- Mission: An org-scoped unit of work, typically associated with a project and optionally a site.
- Resource: An org-scoped entity that can be assigned to reservations (human, asset, service).
- Shift: A scheduled execution unit that references exactly one reservation and a mission.
- Reservation: A time interval that is the source of truth for availability and assignment.
- Conflict: A detected issue tied to a reservation (and optionally a resource), with severity.

## Time as source of truth
Time is the primary record for commitments. Reservations store the canonical interval in UTC with timezone metadata. Other entities (shifts, conflicts) reference reservations to anchor scheduling and validation.

## Canonical enums and where they are defined
- Membership role (owner, admin, member): docs/specs/12_enums_and_states.md
- Resource type (human, asset, service): docs/specs/12_enums_and_states.md
- Shift status (proposed, accepted, confirmed, in_progress, completed, validated, closed): docs/specs/12_enums_and_states.md
- Reservation status (draft, active, cancelled): docs/specs/12_enums_and_states.md
- Conflict severity (critical, high, medium, low): docs/specs/12_enums_and_states.md

## References
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md
- Roadmap: docs/roadmap/roadmap_v1.md
- Core domain: docs/specs/core_domain_model.md
- Time reservation: docs/specs/time_reservation_engine.md
- IAM: docs/specs/iam_minimal.md
- Conflict engine: docs/specs/conflict_engine_minimal.md
