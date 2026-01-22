# Contracts overview

This file summarizes contracts defined under docs/specs/ and maps them to code where evidence exists.
If evidence is missing, status is marked UNKNOWN / NOT IMPLEMENTED YET.

## Contract: Glossary and terms
- Purpose: define canonical terms and avoid synonyms.
- Spec: docs/specs/00_glossary.md
- Implementation: documentation only.
- Status: documentation only.
- Codex MAY change: wording updates that keep terms consistent with the glossary.
- Spec update REQUIRED before: introducing new domain terms or renaming existing terms.

## Contract: Core domain model
- Purpose: define core entities and relationships.
- Spec: docs/specs/core_domain_model.md
- Implementation: planninghub/domain/entities.py, planninghub/domain/value_objects.py
- Status: partial.
- Codex MAY change: internal implementation details that do not alter entities, fields, or invariants.
- Spec update REQUIRED before: changing entities, fields, or relationships.

## Contract: Time reservation engine
- Purpose: define reservation behavior and constraints.
- Spec: docs/specs/time_reservation_engine.md
- Implementation: planninghub/domain/entities.py, planninghub/domain/use_cases/
- Status: partial.
- Codex MAY change: internal calculations that preserve the spec.
- Spec update REQUIRED before: changing reservation fields, states, or invariant rules.

## Contract: IAM minimal
- Purpose: define minimal identity and access constructs.
- Spec: docs/specs/iam_minimal.md
- Implementation: planninghub/application/ports/identity.py, planninghub/application/handlers/identity.py, planninghub/adapters/persistence/
- Status: partial.
- Codex MAY change: adapter implementation details that keep port signatures stable.
- Spec update REQUIRED before: changing identity port contracts or required fields.

## Contract: Conflict engine minimal
- Purpose: define conflict detection and resolution outputs.
- Spec: docs/specs/conflict_engine_minimal.md
- Implementation: planninghub/domain/services/conflict_detection.py, conflict_resolution.py, conflict_orchestrator.py
- Status: partial.
- Codex MAY change: internal conflict algorithms that preserve the outputs defined by the spec.
- Spec update REQUIRED before: changing conflict outcome shapes or severities.

## Contract: Enums and states
- Purpose: define canonical enum values.
- Spec: docs/specs/12_enums_and_states.md
- Implementation: planninghub/domain/value_objects.py
- Status: partial.
- Codex MAY change: internal handling that preserves enum values.
- Spec update REQUIRED before: adding or changing enum values.

## Contract: Invariants minimal
- Purpose: define minimal invariants for core entities.
- Spec: docs/specs/18_invariants_minimal.md
- Implementation: planninghub/domain/entities.py, planninghub/domain/value_objects.py
- Status: partial.
- Codex MAY change: internal validation that preserves invariants.
- Spec update REQUIRED before: changing or removing invariants.

## Contract: Hexagonal architecture
- Purpose: define ports and adapters boundaries.
- Spec: docs/specs/architecture/hexagonal_architecture_contract.md
- Implementation: tools/guards/import_policy_guard.py, planninghub/application/, planninghub/adapters/
- Status: partial (guard enforces some import rules).
- Codex MAY change: adapter internals without altering port contracts.
- Spec update REQUIRED before: changing dependency direction rules.

## Contract: Ports and adapters contracts
- Purpose: define port types, adapter responsibilities, and DTO boundaries.
- Spec: docs/specs/ports_and_adapters_contracts.md
- Implementation: planninghub/application/ports/, planninghub/application/handlers/, planninghub/application/dtos/, planninghub/adapters/
- Status: partial.
- Codex MAY change: adapter or handler implementation details that preserve port signatures.
- Spec update REQUIRED before: changing any port or DTO fields.

## Contract: Frontend UI skeleton
- Purpose: define the minimal static UI skeleton (login and planning dashboard).
- Spec: docs/specs/frontend_ui_skeleton.md
- Implementation: ui/login.html, ui/dashboard.html, ui/styles.css, ui/README.md
- Status: implemented (static).
- Codex MAY change: layout and styling that remain within UX guidance and keep screens in scope.
- Spec update REQUIRED before: adding new UI screens or introducing logic.

## Contract: Identity ports
- Purpose: define inbound and outbound identity ports.
- Spec: docs/specs/ports/identity_ports.md
- Implementation: planninghub/application/ports/identity.py, planninghub/application/handlers/identity.py
- Status: partial.
- Codex MAY change: internal handler logic that preserves DTO shapes.
- Spec update REQUIRED before: changing port request or response fields.

## Contract: Time reservation ports
- Purpose: define time reservation ports.
- Spec: docs/specs/ports/time_reservation_ports.md
- Implementation: planninghub/application/ports/time_reservation.py, planninghub/application/handlers/time_reservation.py
- Status: partial.
- Codex MAY change: handler logic that preserves DTO shapes.
- Spec update REQUIRED before: changing port request or response fields.

## Contract: Conflict ports
- Purpose: define conflict detection ports.
- Spec: docs/specs/ports/conflict_ports.md
- Implementation: planninghub/application/ports/conflict.py, planninghub/application/handlers/conflict.py
- Status: partial.
- Codex MAY change: handler logic that preserves DTO shapes.
- Spec update REQUIRED before: changing port request or response fields.

## Contract: Execution ports
- Purpose: define execution workflow ports.
- Spec: docs/specs/ports/execution_ports.md
- Implementation: UNKNOWN / NOT IMPLEMENTED YET
- Status: not started.
- Codex MAY change: nothing in code (no implementation).
- Spec update REQUIRED before: introducing any execution port code.

## Contract: Finance ports
- Purpose: define finance workflow ports.
- Spec: docs/specs/ports/finance_ports.md
- Implementation: UNKNOWN / NOT IMPLEMENTED YET
- Status: not started.
- Codex MAY change: nothing in code (no implementation).
- Spec update REQUIRED before: introducing any finance port code.

## Contract: Persistence adapters
- Purpose: define persistence adapter responsibilities and boundaries.
- Spec: docs/specs/adapters/persistence_adapters.md
- Implementation: planninghub/adapters/persistence/in_memory.py, planninghub/adapters/persistence/sqlite.py
- Status: partial.
- Codex MAY change: adapter internals that preserve contract behavior.
- Spec update REQUIRED before: changing adapter return shapes or persistence semantics.

## Contract: Real persistence adapter
- Purpose: define contract for a real (non-demo) persistence adapter.
- Spec: docs/specs/persistence_real_adapter_contract.md
- Implementation: UNKNOWN / NOT IMPLEMENTED YET
- Status: not started.
- Codex MAY change: nothing in code (no implementation).
- Spec update REQUIRED before: adding or changing real persistence behavior.

## Contract: Notification adapters
- Purpose: define notification adapter responsibilities.
- Spec: docs/specs/adapters/notification_adapters.md
- Implementation: UNKNOWN / NOT IMPLEMENTED YET
- Status: not started.
- Codex MAY change: nothing in code (no implementation).
- Spec update REQUIRED before: adding notification adapter code.

## Contract: External system adapters
- Purpose: define external system adapter responsibilities.
- Spec: docs/specs/adapters/external_system_adapters.md
- Implementation: UNKNOWN / NOT IMPLEMENTED YET
- Status: not started.
- Codex MAY change: nothing in code (no implementation).
- Spec update REQUIRED before: adding external system adapter code.

## Contract: Package boundaries and public API
- Purpose: define package boundaries and public import surfaces.
- Spec: docs/specs/package_boundaries_and_public_api.md
- Implementation: __init__.py exports and tools/guards/import_policy_guard.py
- Status: partial.
- Codex MAY change: internal modules that remain outside the public API.
- Spec update REQUIRED before: changing public import paths or boundary rules.
