# Spec to tests matrix

This table maps specs to tests based on explicit repository evidence only.

| Spec File | Spec Item (optional) | Test Path(s) | Status | Evidence |
| --- | --- | --- | --- | --- |
| docs/specs/00_glossary.md | - | - | NOT COVERED | No tests reference glossary items. |
| docs/specs/12_enums_and_states.md | Enum value lists | tests/test_domain_contracts.py | COVERED | Enum values asserted in test_enum_values_match_specs. |
| docs/specs/18_invariants_minimal.md | Core invariants | tests/test_domain_contracts.py; tests/test_phase3_ports_adapters_skeleton.py; tests/test_persistence_adapter_contract.py; tests/test_persistence_adapter_in_memory.py | PARTIALLY COVERED | Multiple invariants tested; not all invariants evidenced. |
| docs/specs/adapters/external_system_adapters.md | - | - | NOT COVERED | Placeholder spec with no test evidence. |
| docs/specs/adapters/notification_adapters.md | - | - | NOT COVERED | Placeholder spec with no test evidence. |
| docs/specs/adapters/persistence_adapters.md | Persistence adapter responsibilities | tests/test_persistence_adapter_contract.py; tests/test_persistence_adapter_in_memory.py | PARTIALLY COVERED | Contract behavior and in memory adapter behaviors are tested. |
| docs/specs/architecture/hexagonal_architecture_contract.md | Layer boundaries | - | NOT COVERED | No tests explicitly assert architecture boundaries. |
| docs/specs/conflict_engine_minimal.md | Conflict detection and severity | tests/test_conflict_detection.py; tests/test_conflict_orchestrator.py; tests/test_persistence_adapter_in_memory.py | PARTIALLY COVERED | Overlap detection is tested; full spec not evidenced. |
| docs/specs/core_domain_model.md | Core entity invariants | tests/test_domain_contracts.py | PARTIALLY COVERED | Entity invariants for org scope and shift reservation link are tested. |
| docs/specs/iam_minimal.md | Membership roles and uniqueness | tests/test_domain_contracts.py; tests/test_persistence_adapter_contract.py; tests/test_persistence_adapter_in_memory.py; tests/test_phase3_ports_adapters_skeleton.py | PARTIALLY COVERED | Role values and duplicate membership behavior are tested. |
| docs/specs/index.md | - | - | NOT COVERED | Index only. |
| docs/specs/package_boundaries_and_public_api.md | Public API imports | tests/test_imports.py | PARTIALLY COVERED | Import smoke test asserts public modules import. |
| docs/specs/persistence_real_adapter_contract.md | Persistence adapter contract | tests/test_persistence_adapter_contract.py | PARTIALLY COVERED | Contract tests cover a subset of requirements. |
| docs/specs/ports/conflict_ports.md | Conflict ports shapes | tests/test_persistence_adapter_in_memory.py | PARTIALLY COVERED | Detect and list conflicts exercised via adapter tests. |
| docs/specs/ports/execution_ports.md | - | - | NOT COVERED | No tests for execution ports. |
| docs/specs/ports/finance_ports.md | - | - | NOT COVERED | No tests for finance ports. |
| docs/specs/ports/identity_ports.md | Identity ports shapes | tests/test_phase3_ports_adapters_skeleton.py; tests/test_persistence_adapter_contract.py; tests/test_persistence_adapter_in_memory.py | PARTIALLY COVERED | Handler and persistence behaviors are tested. |
| docs/specs/ports/time_reservation_ports.md | Reservation ports shapes | tests/test_persistence_adapter_contract.py; tests/test_persistence_adapter_in_memory.py; tests/test_fastapi_routes_smoke.py | PARTIALLY COVERED | Create and list reservation flows are exercised. |
| docs/specs/ports_and_adapters_contracts.md | Port and adapter contracts | tests/test_phase3_ports_adapters_skeleton.py; tests/test_http_adapter_mappers.py; tests/test_persistence_adapter_contract.py | PARTIALLY COVERED | Port imports, mapping, and persistence behaviors are tested. |
| docs/specs/time_reservation_engine.md | Reservation invariants | tests/test_domain_contracts.py; tests/test_persistence_adapter_in_memory.py; tests/test_fastapi_routes_smoke.py | PARTIALLY COVERED | Interval and reservation fields exercised in tests. |
