# Coding rules

These rules are mandatory.

## Import direction rules
- Domain MUST NOT import application or infra.
- Application MAY import domain and infra (wiring only).
- Infra MAY import domain and implement ports.
- Adapters MUST depend on ports and DTOs, not the reverse.
- Tests MAY import all layers.

## Layer isolation rules
- Domain contains business logic and invariants.
- Application coordinates domain behavior through ports and handlers.
- Adapters handle IO and mapping only.
- Infra contains wiring, configuration, and in-memory helpers.

## Business logic definition
Business logic includes:
- invariants
- conflict detection and resolution
- reservation state transitions
- validation beyond simple type checks

Business logic MUST live in domain or application layers only.

## Decision stop rule
You MUST stop and write a decision doc if:
- two authority sources conflict
- a required spec is missing or ambiguous
- you need to change architecture boundaries

## Naming rules
- Files: lower_snake_case.py
- Tests: test_<topic>.py
- Classes: PascalCase
- Functions: lower_snake_case

## ASCII-only rule
- All documentation and identifiers MUST use ASCII only.

## Determinism rules
- Tests MUST be deterministic.
- Adapters MUST NOT introduce nondeterministic behavior without a spec.

## Prohibited patterns
- Do NOT add business logic in adapters.
- Do NOT add try/except around imports.
- Do NOT change public API without a spec update.
