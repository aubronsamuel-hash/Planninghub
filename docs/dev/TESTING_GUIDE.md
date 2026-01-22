# Testing guide

## Run all tests
- python -m pytest

## Run a single file or folder
- python -m pytest tests/test_domain_contracts.py
- python -m pytest tests/contracts/

## Test categories

### Invariant tests
- Purpose: enforce domain invariants and canonical enums.
- Locations:
  - tests/test_domain_contracts.py

### Domain tests
- Purpose: domain services and use cases.
- Locations:
  - tests/test_conflict_detection.py
  - tests/test_conflict_orchestrator.py
  - tests/test_conflict_outcomes.py
  - tests/test_conflict_resolution.py
  - tests/test_evaluate_reservation_use_case.py

### Adapter tests
- Purpose: adapter DTO mapping, transport, and persistence adapters.
- Locations:
  - tests/test_http_adapter_mappers.py
  - tests/test_cli_adapter_evaluate_incoming_reservation.py
  - tests/test_cli_smoke.py
  - tests/test_fastapi_routes_smoke.py
  - tests/test_persistence_adapter_contract.py
  - tests/test_persistence_adapter_in_memory.py
  - tests/contracts/

### Integration tests (if any)
- UNKNOWN / NOT IMPLEMENTED YET
- Current evidence suggests no explicit integration test suite beyond adapter smoke tests.

## Naming conventions
- Use test_*.py at repo root or under tests/ subfolders.
- Prefer descriptive file names aligned with a single contract or use case.

## Where new tests MUST go
- Domain invariants or value object rules: tests/test_domain_contracts.py or a new tests/test_domain_*.py file.
- Domain use cases: tests/test_*use_case*.py.
- Application handler or port contracts: tests/test_application_*.py or tests/test_phase3_ports_adapters_skeleton.py.
- Adapter behavior: tests/test_*adapter*.py or tests/contracts/.
- Infrastructure utilities: tests/test_*in_memory*.py.

## Semantics of failures
- A failing test means a contract or invariant is broken.
- Do NOT change tests to match code without updating the corresponding spec.

## Rules
- No test without a spec update.
- No behavior test without a contract or invariant reference.

## Examples (paths only)
- tests/test_phase3_ports_adapters_skeleton.py
- tests/test_persistence_adapter_contract.py
- tests/test_http_adapter_mappers.py
