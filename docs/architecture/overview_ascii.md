# Architecture Overview (ASCII)

## 1. Purpose
This document provides a one page, repo based architecture overview.
It is an orientation aid, not a full technical specification.
It maps the diagram to concrete folders and specs that exist today.
This diagram reflects repository evidence, not future intent.

## 2. Evidence Pointers (Mandatory)
- AGENT.md
- docs/Planning_hub_architecture_vision_produit_v_1.md
- docs/specs/architecture/hexagonal_architecture_contract.md
- docs/specs/ports_and_adapters_contracts.md
- docs/specs/persistence_real_adapter_contract.md
- docs/specs/ports/
- docs/specs/adapters/
- planninghub/domain/
- planninghub/application/
- planninghub/adapters/
- planninghub/infra/
- tests/

## 3. ASCII Architecture Diagram (Mandatory)
+--------------------------------------------------------------------+
|                           PlanningHub                               |
|                                                                    |
|  +-------------------------+      +------------------------------+ |
|  | Docs (authority)        |      | Tests                        | |
|  | - docs/vision           |      | - tests/                     | |
|  | - docs/specs            |      |                              | |
|  | - docs/roadmap          |      +------------------------------+ |
|  +-------------------------+                                      |
|                                                                    |
|  +-------------------------+      +------------------------------+ |
|  | Domain                  |<---->| Application                  | |
|  | - entities              |      | - ports                      | |
|  | - value objects         |      | - handlers, dtos             | |
|  | - domain services       |      |                              | |
|  +-------------------------+      +------------------------------+ |
|              ^                               ^                     |
|              |                               |                     |
|  +-------------------------+      +------------------------------+ |
|  | Adapters                |      | Infra / wiring               | |
|  | - cli                   |      | - wiring, config             | |
|  | - http (fastapi)        |      |                              | |
|  | - persistence           |      +------------------------------+ |
|  +-------------------------+                                      |
+--------------------------------------------------------------------+

## 4. Layer Responsibilities (Short, Deterministic)
Docs (authority)
- MUST capture vision, roadmap, specs, and governance constraints.
- MUST NOT claim runtime behavior beyond what code implements.

Tests
- MUST validate contracts and observable behavior in the repo.
- MUST NOT define production wiring or new runtime dependencies.

Domain
- MUST contain entities, value objects, and domain level services.
- MUST NOT depend on adapters, frameworks, or IO concerns.

Application
- MUST define ports, handlers, and DTOs used by use cases.
- MUST NOT embed adapter specific logic or persistence details.

Adapters
- MUST implement ports and translate external IO to application DTOs.
- MUST NOT introduce new business rules or domain invariants.

Infra / wiring
- MUST compose configuration and wiring between adapters and core.
- MUST NOT define new domain rules or use case behavior.

## 5. Repository Mapping Table
Component | Repo path(s) | Notes
Domain | planninghub/domain/ | entities, value objects, services
Application | planninghub/application/ | ports, handlers, dtos
Adapters | planninghub/adapters/ | cli, http, persistence
Infra / wiring | planninghub/infra/ | config, wiring helpers
Docs (authority) | docs/vision/, docs/specs/, docs/roadmap/ | governance and specs
Tests | tests/ | contract and adapter tests

## 6. Known Gaps (Strictly Evidenced)
- None explicitly documented in the referenced files.
