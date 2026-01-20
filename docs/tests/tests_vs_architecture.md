# Tests vs architecture

## Layer mapping
- Domain
  - tests/test_domain_contracts.py
  - tests/test_conflict_detection.py
  - tests/test_conflict_orchestrator.py
  - tests/test_conflict_outcomes.py
  - tests/test_conflict_resolution.py
  - tests/test_evaluate_reservation_use_case.py
- Application
  - tests/test_application_handler_evaluate_incoming_reservation.py
  - tests/test_phase3_ports_adapters_skeleton.py
  - tests/test_application_wiring.py
- Adapters
  - tests/test_http_adapter_mappers.py
  - tests/test_fastapi_routes_smoke.py
  - tests/test_cli_adapter_evaluate_incoming_reservation.py
  - tests/test_cli_smoke.py
  - tests/test_persistence_adapter_contract.py
  - tests/test_persistence_adapter_in_memory.py
- Infrastructure (in memory repositories)
  - tests/test_repositories_in_memory.py
  - tests/test_reservation_repository_in_memory.py
- Docs/spec contracts (explicit spec alignment)
  - docs/specs/12_enums_and_states.md -> tests/test_domain_contracts.py
  - docs/specs/18_invariants_minimal.md -> tests/test_domain_contracts.py,
    tests/test_phase3_ports_adapters_skeleton.py,
    tests/test_persistence_adapter_contract.py,
    tests/test_persistence_adapter_in_memory.py

## ADR protection mapping
- ADR-0001 (ports and adapters architecture)
  - tests/test_phase3_ports_adapters_skeleton.py
  - tests/test_persistence_adapter_contract.py
  - tests/test_http_adapter_mappers.py
- ADR-0002 (invariant enforcement boundaries)
  - tests/test_domain_contracts.py
  - tests/test_phase3_ports_adapters_skeleton.py
  - tests/test_persistence_adapter_in_memory.py
- ADR-0003 and ADR-0004: UNKNOWN (no test evidence found).
