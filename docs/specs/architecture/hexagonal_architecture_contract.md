# Spec: Hexagonal architecture contract (minimal)

## Purpose
Define the contract between application core and infrastructure using ports and adapters.

## Core principles
- The application core owns domain models, invariants, and port definitions.
- Adapters implement ports without adding business logic.
- Dependencies point inward: adapters depend on ports, not the reverse.

## Layer boundaries
### Domain
- Entities, value objects, and invariants.
- No dependencies on application or infrastructure.

### Application
- Ports (command/query definitions).
- Application services that coordinate domain rules without infrastructure details.

### Infrastructure
- Adapters that implement ports (persistence, notification, external systems).
- No domain rule changes.

## Port types
- Inbound ports: commands and queries exposed by the application core.
- Outbound ports: required services needed by the core (e.g., persistence).

## Adapter constraints
- Adapters MUST preserve data shapes defined by port specs.
- Adapters MUST enforce only the invariants already defined in domain specs.
- Adapters MUST be replaceable without changing the application core.

## Explicit NON-responsibilities
- No framework selection or wiring.
- No API or transport protocol definitions.
- No workflow orchestration.

## Traceability
- Roadmap: docs/roadmap/roadmap_v1.md (Phase 2)
- Specs: docs/specs/ports/*, docs/specs/adapters/*
