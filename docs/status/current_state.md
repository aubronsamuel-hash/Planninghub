# Current state

## Evidence sources
- docs/audits/implementation_readiness.md
- docs/specs/core_domain_model.md
- docs/specs/ports_and_adapters_contracts.md
- docs/specs/persistence_real_adapter_contract.md
- docs/roadmap/roadmap_v1.md

## What exists today
- Documented core entities and invariants for the foundation domain model.
- Documented domain contracts for time reservation, IAM, and conflict detection.
- Documented ports and adapters contracts for the application layer.
- Implementation readiness audit reports Phase 3 and Phase 4 as done with referenced ports, adapters, and tests.

## What is intentionally missing
- Scheduling heuristics, persistence implementation, and framework wiring are explicitly out of scope in earlier phases.
- Phase 5+ capabilities (execution workflows, resource matching, financial intelligence, automation, marketplace, notifications, analytics, mobile offline, security, integrations) are future placeholders.

## What is blocked by design
- Any implementation that conflicts with the canonical vision or roadmap stop conditions must halt until a decision is recorded.
- Any capability outside the active phase is blocked unless the roadmap is updated with evidence and decisions.
