# Roadmap v1 (authoritative execution contract)

## Authority and scope
This roadmap is the single source of execution truth for PlanningHub work. It is
subordinate only to AGENT.md and the canonical vision doc at
`docs/Planning_hub_architecture_vision_produit_v_1.md`. It reconciles docs and
code to declare what is DONE, what is AUTHORIZED NEXT, and what is FORBIDDEN.

If authority is missing or conflicting, this roadmap must declare a DECISION
REQUIRED section and block further work until resolved.

## Status definitions
- DONE: Implemented and aligned with authority.
- AUTHORIZED NEXT: The only work Codex may start next.
- BLOCKED: Work cannot proceed due to missing inputs.
- FORBIDDEN: Not authorized or conflicts with authority.

## Phase 0: Docs and governance baseline

### Step 0.1: Roadmap and index presence
- STATUS: DONE
- EVIDENCE: docs/roadmap/roadmap_v1.md, docs/roadmap/index.md
- ALLOWED ACTIONS: Maintain roadmap and index links.
- FORBIDDEN ACTIONS: Change code or specs.
- STOP CONDITION: Roadmap and index are present and linked.

### Step 0.2: Specs index presence
- STATUS: DONE
- EVIDENCE: docs/specs/index.md
- ALLOWED ACTIONS: Maintain the specs index only.
- FORBIDDEN ACTIONS: Add or change specs while authority is unclear.
- STOP CONDITION: Specs index lists current specs.

### Step 0.3: Implementation readiness audit
- STATUS: DONE
- EVIDENCE: docs/audits/implementation_readiness.md
- ALLOWED ACTIONS: Update audit when roadmap changes.
- FORBIDDEN ACTIONS: Implement code without audit alignment.
- STOP CONDITION: Audit matches the roadmap state.

### Step 0.4: Authority reconciliation decisions
- STATUS: AUTHORIZED NEXT
- EVIDENCE: docs/specs/persistence_real_adapter_contract.md,
  planninghub/adapters/persistence/sqlite.py,
  docs/specs/frontend_ui_skeleton.md, ui/login.html
- ALLOWED ACTIONS: Create decisions to resolve authority gaps listed in the
  DECISION REQUIRED section of this roadmap.
- FORBIDDEN ACTIONS: Implement or expand unauthorized features before decisions
  are recorded.
- STOP CONDITION: Decisions are recorded that resolve all authority gaps.

## Phase 1: Domain contracts skeleton

### Step 1.1: Core domain model
- STATUS: DONE
- EVIDENCE: docs/specs/core_domain_model.md
- ALLOWED ACTIONS: Clarify doc wording only.
- FORBIDDEN ACTIONS: Add new domain rules or entities.
- STOP CONDITION: Core entities and invariants are documented.

### Step 1.2: Identity and access management
- STATUS: DONE
- EVIDENCE: docs/specs/iam_minimal.md
- ALLOWED ACTIONS: Clarify doc wording only.
- FORBIDDEN ACTIONS: Add auth flows or persistence decisions.
- STOP CONDITION: IAM minimal contract is documented.

### Step 1.3: Time reservation engine
- STATUS: DONE
- EVIDENCE: docs/specs/time_reservation_engine.md
- ALLOWED ACTIONS: Clarify doc wording only.
- FORBIDDEN ACTIONS: Add scheduling heuristics or workflows.
- STOP CONDITION: Reservation contract and rules are documented.

### Step 1.4: Conflict engine minimal
- STATUS: DONE
- EVIDENCE: docs/specs/conflict_engine_minimal.md
- ALLOWED ACTIONS: Clarify doc wording only.
- FORBIDDEN ACTIONS: Add conflict resolution strategies.
- STOP CONDITION: Conflict detection contract is documented.

### Step 1.5: Enums and states
- STATUS: DONE
- EVIDENCE: docs/specs/12_enums_and_states.md
- ALLOWED ACTIONS: Clarify doc wording only.
- FORBIDDEN ACTIONS: Add new state machines or workflows.
- STOP CONDITION: Enumerations are listed.

### Step 1.6: Minimal invariants
- STATUS: DONE
- EVIDENCE: docs/specs/18_invariants_minimal.md
- ALLOWED ACTIONS: Clarify doc wording only.
- FORBIDDEN ACTIONS: Add new invariants or validation rules.
- STOP CONDITION: Minimal invariants are documented.

## Phase 2: Ports and adapters contracts

### Step 2.1: Ports and adapters overview
- STATUS: DONE
- EVIDENCE: docs/specs/ports_and_adapters_contracts.md
- ALLOWED ACTIONS: Clarify doc wording only.
- FORBIDDEN ACTIONS: Add new ports or adapters.
- STOP CONDITION: Ports and adapter boundaries are documented.

### Step 2.2: Identity, reservation, and conflict ports
- STATUS: DONE
- EVIDENCE: docs/specs/ports/identity_ports.md,
  docs/specs/ports/time_reservation_ports.md,
  docs/specs/ports/conflict_ports.md
- ALLOWED ACTIONS: Clarify doc wording only.
- FORBIDDEN ACTIONS: Add new port methods.
- STOP CONDITION: Port method contracts are documented.

### Step 2.3: Persistence adapter boundaries
- STATUS: DONE
- EVIDENCE: docs/specs/adapters/persistence_adapters.md
- ALLOWED ACTIONS: Clarify doc wording only.
- FORBIDDEN ACTIONS: Select databases or schemas.
- STOP CONDITION: Adapter responsibilities are documented.

### Step 2.4: Placeholder ports and adapters for future capabilities
- STATUS: FORBIDDEN
- EVIDENCE: docs/specs/ports/execution_ports.md,
  docs/specs/ports/finance_ports.md,
  docs/specs/adapters/notification_adapters.md,
  docs/specs/adapters/external_system_adapters.md
- ALLOWED ACTIONS: Keep placeholders clearly marked as FUTURE only.
- FORBIDDEN ACTIONS: Implement any execution, finance, notification, or
  integration logic.
- STOP CONDITION: Remains blocked until Phase 5 authority exists.

## Phase 3: Persistence adapters implementation (skeleton)

### Step 3.1: In-memory persistence adapter
- STATUS: DONE
- EVIDENCE: planninghub/adapters/persistence/in_memory.py,
  planninghub/infra/repositories_in_memory.py,
  tests/test_persistence_adapter_in_memory.py,
  tests/test_phase3_ports_adapters_skeleton.py
- ALLOWED ACTIONS: Maintain tests and adapter behavior to match specs.
- FORBIDDEN ACTIONS: Add new domain rules or persistence features.
- STOP CONDITION: In-memory adapter passes existing tests.

### Step 3.2: SQLite persistence adapter with schema
- STATUS: FORBIDDEN
- EVIDENCE: planninghub/adapters/persistence/sqlite.py,
  planninghub/infra/repositories_sqlite.py,
  tests/test_persistence_adapter_contract.py,
  tests/test_repositories_sqlite.py
- ALLOWED ACTIONS: Do not modify until authority is clarified.
- FORBIDDEN ACTIONS: Expand schemas, migrations, or persistence behavior.
- STOP CONDITION: Decision recorded to authorize or remove sqlite schema usage.

## Phase 4: HTTP adapter wiring

### Step 4.1: HTTP mapping and routing
- STATUS: DONE
- EVIDENCE: planninghub/adapters/http/mappers.py,
  planninghub/adapters/fastapi_app/routes.py,
  planninghub/adapters/http/server.py
- ALLOWED ACTIONS: Maintain adapter wiring to match ports.
- FORBIDDEN ACTIONS: Add new endpoints or business rules.
- STOP CONDITION: HTTP adapters remain minimal and aligned with ports.

### Step 4.2: HTTP adapter tests
- STATUS: DONE
- EVIDENCE: tests/test_http_adapter_mappers.py,
  tests/test_http_evaluate_reservation_api.py
- ALLOWED ACTIONS: Maintain tests aligned to existing endpoints.
- FORBIDDEN ACTIONS: Add tests for unauthorized endpoints.
- STOP CONDITION: HTTP adapter tests remain green.

## Phase 5: UI skeleton (static)

### Step 5.1: Static UI skeleton
- STATUS: FORBIDDEN
- EVIDENCE: docs/specs/frontend_ui_skeleton.md, ui/login.html,
  ui/dashboard.html, ui/styles.css, ui/README.md
- ALLOWED ACTIONS: No changes until authority is clarified.
- FORBIDDEN ACTIONS: Add interactivity, API wiring, or new screens.
- STOP CONDITION: Decision recorded to authorize or remove the UI skeleton.

## Phase 6: Future capabilities (placeholders only)

### Step 6.1: Future execution, finance, notifications, integrations
- STATUS: FORBIDDEN
- EVIDENCE: docs/specs/ports/execution_ports.md,
  docs/specs/ports/finance_ports.md,
  docs/specs/adapters/notification_adapters.md,
  docs/specs/adapters/external_system_adapters.md
- ALLOWED ACTIONS: None beyond maintaining placeholder labels.
- FORBIDDEN ACTIONS: Implement or spec additional behavior.
- STOP CONDITION: Remains blocked until a new roadmap update authorizes work.

## DECISION REQUIRED
Authority gaps must be resolved before any new implementation work.

1) Persistence authority mismatch
   - Evidence: docs/specs/adapters/persistence_adapters.md forbids database and
     schema selection, while planninghub/adapters/persistence/sqlite.py and
     planninghub/infra/repositories_sqlite.py implement sqlite schemas.
   - Decision required: authorize sqlite schema usage or remove/rollback sqlite
     persistence implementation.

2) UI skeleton authority mismatch
   - Evidence: docs/specs/frontend_ui_skeleton.md and ui/ exist, but the prior
     roadmap did not authorize a UI phase.
   - Decision required: authorize the UI skeleton as an approved phase or remove
     the UI artifacts.

## Final checks
- No spec files were modified or created.
- No code files were touched.
- This roadmap is the single source of execution truth.
