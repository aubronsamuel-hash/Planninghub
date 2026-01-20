# Testing philosophy

## Purpose
Tests exist to lock contracts and invariants for the foundation skeleton. They verify
canonical enum values, core domain invariants, conflict detection behavior, and adapter
contracts so that domain rules and port expectations do not drift. Evidence:
- tests/test_domain_contracts.py
- tests/test_conflict_detection.py
- tests/test_conflict_orchestrator.py
- tests/test_conflict_outcomes.py
- tests/test_conflict_resolution.py
- tests/test_evaluate_reservation_use_case.py
- tests/test_application_handler_evaluate_incoming_reservation.py
- tests/test_phase3_ports_adapters_skeleton.py
- tests/test_persistence_adapter_contract.py
- tests/test_persistence_adapter_in_memory.py
- tests/test_http_adapter_mappers.py
- tests/test_fastapi_routes_smoke.py
- tests/test_cli_adapter_evaluate_incoming_reservation.py
- tests/test_imports.py

## Non-goals
Non-goals are taken from existing specs. Tests do not claim coverage for:
- Workflow automation or lifecycle orchestration (docs/specs/core_domain_model.md).
- Recurrence rules or buffers in time reservation (docs/specs/time_reservation_engine.md).
- Automatic resolution actions beyond minimal conflict outputs
  (docs/specs/conflict_engine_minimal.md).
- External integrations or notification delivery rules
  (docs/specs/adapters/external_system_adapters.md,
  docs/specs/adapters/notification_adapters.md).
If additional non-goals exist, they are UNKNOWN.

## Determinism
Repository rules for test determinism are not explicitly documented. Determinism
expectations exist for adapters and ports (docs/specs/ports_and_adapters_contracts.md,
docs/specs/persistence_real_adapter_contract.md), but a repo wide test determinism
policy is UNKNOWN.

## Evidence of protected contracts
Key specs and ADRs referenced by tests:
- docs/specs/12_enums_and_states.md
- docs/specs/18_invariants_minimal.md
- docs/specs/time_reservation_engine.md
- docs/specs/conflict_engine_minimal.md
- docs/specs/iam_minimal.md
- docs/specs/persistence_real_adapter_contract.md
- docs/specs/ports_and_adapters_contracts.md
- docs/specs/package_boundaries_and_public_api.md
- docs/architecture/decisions/ADR-0001-ports-and-adapters-architecture.md
- docs/architecture/decisions/ADR-0002-invariant-enforcement-boundaries.md
