# ADR-0002: Invariant enforcement boundaries

Status: ACCEPTED

Context:
- The application core owns domain models and invariants.
- Adapters must enforce only invariants defined in domain specs and add no business logic.
- Evidence: docs/specs/architecture/hexagonal_architecture_contract.md
- Evidence: docs/specs/18_invariants_minimal.md

Decision:
- Invariants are defined in domain specs and owned by the application core, and adapters only enforce those invariants.

Rationale: NOT DOCUMENTED

Consequences:
- Invariants are listed in docs/specs/18_invariants_minimal.md for cross-spec alignment.
- Adapter constraints reference invariants already defined in domain specs.

References:
- docs/specs/architecture/hexagonal_architecture_contract.md
- docs/specs/18_invariants_minimal.md
- docs/specs/ports_and_adapters_contracts.md
