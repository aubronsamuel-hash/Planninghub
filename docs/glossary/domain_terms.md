# Domain Terms (Locked)

## Organization

Definition:
- An org-scoped tenant boundary for data and access that owns scoped entities.

Scope:
- Domain

Not:
- UNKNOWN

Evidence:
- docs/specs/00_glossary.md
- docs/specs/iam_minimal.md
- docs/specs/core_domain_model.md

## User

Definition:
- A global identity that can belong to organizations via memberships.

Scope:
- Domain

Not:
- Not scoped to a single organization (User is global).

Evidence:
- docs/specs/00_glossary.md
- docs/specs/iam_minimal.md
- docs/specs/core_domain_model.md

## Membership

Definition:
- The link between a user and an organization, including the role used for access scope.

Scope:
- Domain

Not:
- UNKNOWN

Evidence:
- docs/specs/00_glossary.md
- docs/specs/iam_minimal.md
- docs/specs/core_domain_model.md

## Project

Definition:
- An org-scoped container for missions and planning context.

Scope:
- Domain

Not:
- UNKNOWN

Evidence:
- docs/specs/00_glossary.md
- docs/specs/core_domain_model.md

## Site

Definition:
- An org-scoped location descriptor for missions and shifts.

Scope:
- Domain

Not:
- UNKNOWN

Evidence:
- docs/specs/00_glossary.md
- docs/specs/core_domain_model.md

## Mission

Definition:
- An org-scoped unit of work associated with a project and optionally a site.

Scope:
- Domain

Not:
- UNKNOWN

Evidence:
- docs/specs/00_glossary.md
- docs/specs/core_domain_model.md

## Resource

Definition:
- An org-scoped entity that can be assigned to reservations, described as a person or asset.

Scope:
- Domain

Not:
- UNKNOWN

Evidence:
- docs/specs/00_glossary.md
- docs/specs/time_reservation_engine.md
- docs/specs/core_domain_model.md

## Shift

Definition:
- A scheduled execution unit that references exactly one reservation and a mission.

Scope:
- Domain

Not:
- UNKNOWN

Evidence:
- docs/specs/00_glossary.md
- docs/specs/core_domain_model.md

## Reservation

Definition:
- A time interval that is the source of truth for availability and assignment.

Scope:
- Domain

Not:
- UNKNOWN

Evidence:
- docs/specs/00_glossary.md
- docs/specs/time_reservation_engine.md

## Conflict

Definition:
- A detected overlap or rule violation tied to a reservation, with severity.

Scope:
- Domain

Not:
- UNKNOWN

Evidence:
- docs/specs/00_glossary.md
- docs/specs/conflict_engine_minimal.md

## Invariant

Definition:
- A rule listed under an Invariants section in the specs.

Scope:
- Documentation

Not:
- UNKNOWN

Evidence:
- docs/specs/core_domain_model.md
- docs/specs/time_reservation_engine.md
- docs/specs/conflict_engine_minimal.md

## Port

Definition:
- A command or query definition exposed by the application core.

Scope:
- Application

Not:
- UNKNOWN

Evidence:
- docs/specs/architecture/hexagonal_architecture_contract.md
- docs/specs/ports_and_adapters_contracts.md

## Adapter

Definition:
- An infrastructure component that implements ports and translates external IO to application DTOs.

Scope:
- Documentation

Not:
- Not a place for new business logic (adapters implement ports without adding business logic).

Evidence:
- docs/specs/architecture/hexagonal_architecture_contract.md
- docs/architecture/overview_ascii.md
