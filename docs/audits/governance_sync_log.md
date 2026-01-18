# Governance Sync Log

Date: 2026-01-17

## Summary of changes
- Removed docs/agents/README.md from deprecated listings to keep the entry documentation active.
- Removed duplicate DO NOT DO content in implementation readiness to keep a single final gate.
- Decision 001 created to formalize the canonical vision document and unblock readiness.
- Added baseline Python tooling (pyproject.toml, ruff, pytest) and CI workflow.
- Added/updated glossary, enums/states, and invariants specs to unblock entity implementation.

## Rationale
These updates align governance with the vision doc and enforce a real readiness gate before implementation work.

## References
- docs/Planning_hub_architecture_vision_produit_v_1.md
- docs/audits/implementation_readiness.md
- docs/roadmap/roadmap_v1.md
- docs/specs/core_domain_model.md
- docs/specs/time_reservation_engine.md
- docs/specs/iam_minimal.md
- docs/specs/conflict_engine_minimal.md

---

Date: 2026-01-18

## Summary of changes
- Tightened persistence adapter contract with explicit write atomicity, concurrency,
  and error taxonomy requirements.

## Rationale
Clarifies implementation-ready guarantees for atomicity, concurrency, and error
handling without selecting a storage technology.

## References
- docs/specs/persistence_real_adapter_contract.md
