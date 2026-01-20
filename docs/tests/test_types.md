# Test types

This list classifies test types present under tests/. Only types with evidence
are listed.

## Domain contract and invariant tests
Definition: Validate canonical enum values and core entity invariants.
Scope: Domain.
Evidence:
- tests/test_domain_contracts.py
Must NOT:
- Enforce workflow automation or lifecycle orchestration (docs/specs/core_domain_model.md).

## Domain service behavior tests
Definition: Exercise conflict detection, conflict resolution, and domain use cases.
Scope: Domain.
Evidence:
- tests/test_conflict_detection.py
- tests/test_conflict_orchestrator.py
- tests/test_conflict_outcomes.py
- tests/test_conflict_resolution.py
- tests/test_evaluate_reservation_use_case.py
Must NOT:
- Automatic resolution actions beyond minimal conflict outputs
  (docs/specs/conflict_engine_minimal.md).

## Application handler and DTO contract tests
Definition: Validate application handlers and DTO immutability and request
validation behavior.
Scope: Application.
Evidence:
- tests/test_application_handler_evaluate_incoming_reservation.py
- tests/test_phase3_ports_adapters_skeleton.py
Must NOT:
- Introduce infrastructure specific behavior beyond port contracts
  (docs/specs/architecture/hexagonal_architecture_contract.md).

## Adapter DTO mapping tests
Definition: Validate adapter request and response mapping to application ports.
Scope: Adapter.
Evidence:
- tests/test_http_adapter_mappers.py
Must NOT:
- Add business logic in adapters (docs/specs/architecture/hexagonal_architecture_contract.md).

## Adapter transport smoke tests
Definition: Exercise CLI and HTTP adapter surfaces end to end within the repo.
Scope: Adapter.
Evidence:
- tests/test_cli_adapter_evaluate_incoming_reservation.py
- tests/test_cli_smoke.py
- tests/test_fastapi_routes_smoke.py
Must NOT:
- Add business logic in adapters (docs/specs/architecture/hexagonal_architecture_contract.md).

## Persistence adapter contract tests
Definition: Validate persistence ports behavior for in memory and sqlite adapters.
Scope: Adapter.
Evidence:
- tests/test_persistence_adapter_contract.py
- tests/test_persistence_adapter_in_memory.py
Must NOT:
- Introduce new business rules or scheduling logic
  (docs/specs/persistence_real_adapter_contract.md).

## In memory repository tests
Definition: Validate in memory repository list and filter behavior.
Scope: Infrastructure.
Evidence:
- tests/test_repositories_in_memory.py
- tests/test_reservation_repository_in_memory.py
Must NOT:
- UNKNOWN (no explicit repo rule found).

## Import and wiring smoke tests
Definition: Validate module imports and wiring configuration.
Scope: Application / Infrastructure.
Evidence:
- tests/test_imports.py
- tests/test_application_wiring.py
- tests/test_app_demo.py
Must NOT:
- UNKNOWN (no explicit repo rule found).
