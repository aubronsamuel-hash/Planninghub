# ADR-0001: Ports and adapters architecture

Status: ACCEPTED

Context:
- The architecture contract defines a hexagonal approach with ports and adapters.
- Adapters depend on ports and do not add business logic.
- Evidence: docs/specs/architecture/hexagonal_architecture_contract.md
- Evidence: docs/specs/ports_and_adapters_contracts.md

Decision:
- PlanningHub uses a ports and adapters (hexagonal) architecture with inward dependencies.

Rationale: NOT DOCUMENTED

Consequences:
- Port definitions live under planninghub/application/ports and are documented in specs.
- Adapter contracts and implementations are documented under docs/specs/adapters and planninghub/adapters.
- Application, domain, and infrastructure layers are separated in documentation and code layout.

References:
- docs/specs/architecture/hexagonal_architecture_contract.md
- docs/specs/ports_and_adapters_contracts.md
- docs/specs/index.md
- planninghub/application/ports
- planninghub/adapters
