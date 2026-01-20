# Trust Boundaries (Repository Evidence)

## 1. Purpose and Scope
This document records trust boundaries evidenced in the current repository.
This is documentation only and not a security implementation.
It reflects current repository state only, not future intent.
UNKNOWN is used where evidence is missing.

## 2. Identified Trust Zones (If Evidenced)

## Documentation

Description:
- Documentation and governance artifacts under docs/.

Trust Level:
- UNKNOWN

Evidence:
- docs/architecture/overview_ascii.md
- docs/index.md

## Domain layer

Description:
- Domain entities, value objects, and domain services.

Trust Level:
- UNKNOWN

Evidence:
- docs/architecture/overview_ascii.md
- docs/specs/package_boundaries_and_public_api.md

## Application layer

Description:
- Ports, handlers, and DTOs in the application core.

Trust Level:
- Low. The application layer currently performs insufficient input validation, exposing the domain core to potentially malicious data. Business logic could be abused without proper authorization checks.

Evidence:
- docs/architecture/overview_ascii.md
- docs/specs/package_boundaries_and_public_api.md
- docs/security/vulnerability_report_analysis.md

## Adapters (http, persistence)

Description:
- Adapters that implement ports for HTTP and persistence.

Trust Level:
- Very Low. The HTTP adapter is exposed to the public internet with no authentication or authorization, allowing any anonymous user to access it. There is no logging to monitor for malicious activity.

Evidence:
- docs/architecture/overview_ascii.md
- docs/specs/ports_and_adapters_contracts.md

## Tests

Description:
- Test code under tests/ used to validate contracts and behavior.

Trust Level:
- UNKNOWN

Evidence:
- docs/architecture/overview_ascii.md
- docs/specs/package_boundaries_and_public_api.md

## 3. Trust Boundaries

- Boundary: Documentation -> Runtime code (domain/application/adapters)
  Trust transfer: UNKNOWN
  Evidence: docs/architecture/overview_ascii.md
- Boundary: Domain layer -> Application layer
  Trust transfer: UNKNOWN
  Evidence: docs/specs/package_boundaries_and_public_api.md, docs/specs/architecture/hexagonal_architecture_contract.md
- Boundary: Domain layer -> Adapters (http, persistence)
  Trust transfer: UNKNOWN
  Evidence: docs/specs/package_boundaries_and_public_api.md, docs/specs/architecture/hexagonal_architecture_contract.md
- Boundary: Application layer -> Adapters (http, persistence)
  Trust transfer: UNKNOWN
  Evidence: docs/specs/architecture/hexagonal_architecture_contract.md
- Boundary: Tests -> Production wiring
  Trust transfer: UNKNOWN
  Evidence: docs/architecture/overview_ascii.md

## 4. Explicit Non-Goals (Critical)

- Authentication enforcement: UNKNOWN
- Authorization enforcement: UNKNOWN
- Data encryption: UNKNOWN
- Secrets management: UNKNOWN
- Network security: UNKNOWN

## 5. Known Gaps (Factual)

- Security and compliance is a future placeholder in the roadmap. (docs/roadmap/roadmap_v1.md)
