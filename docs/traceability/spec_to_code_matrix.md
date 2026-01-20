# Spec to Code Traceability Matrix

This table lists specs under docs/specs and their direct code references when documented. Mappings are limited to evidenced file paths.

| Spec File | Spec Item (if applicable) | Code Path | Status | Evidence |
| --- | --- | --- | --- | --- |
| docs/specs/00_glossary.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/12_enums_and_states.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/18_invariants_minimal.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/adapters/external_system_adapters.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/adapters/notification_adapters.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/adapters/persistence_adapters.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/architecture/hexagonal_architecture_contract.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/conflict_engine_minimal.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/core_domain_model.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/iam_minimal.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/package_boundaries_and_public_api.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/persistence_real_adapter_contract.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/ports/conflict_ports.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/ports/execution_ports.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/ports/finance_ports.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/ports/identity_ports.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/ports/time_reservation_ports.md | ALL | - | NOT IMPLEMENTED | - |
| docs/specs/ports_and_adapters_contracts.md | ALL | planninghub/application/ports/identity.py<br>planninghub/application/ports/time_reservation.py<br>planninghub/application/ports/conflict.py<br>planninghub/application/ports/persistence.py<br>planninghub/application/handlers/identity.py<br>planninghub/application/handlers/time_reservation.py<br>planninghub/application/handlers/conflict.py<br>planninghub/adapters/persistence/in_memory.py<br>planninghub/infra/repositories_in_memory.py<br>planninghub/adapters/http/mappers.py | IMPLEMENTED | planninghub/application/ports/identity.py<br>planninghub/application/ports/time_reservation.py<br>planninghub/application/ports/conflict.py<br>planninghub/application/ports/persistence.py<br>planninghub/application/handlers/identity.py<br>planninghub/application/handlers/time_reservation.py<br>planninghub/application/handlers/conflict.py<br>planninghub/adapters/persistence/in_memory.py<br>planninghub/infra/repositories_in_memory.py<br>planninghub/adapters/http/mappers.py |
| docs/specs/time_reservation_engine.md | ALL | - | NOT IMPLEMENTED | - |
