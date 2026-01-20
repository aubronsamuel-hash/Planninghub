# Roadmap v1

## Purpose and authority
This roadmap is the canonical plan for moving from vision to implementation. It defines phases, dependencies, and stop conditions. It is subordinate to the vision doc and referenced by audits and specs.

## Status references
- [Current state](../status/current_state.md)
- [Phase status](../status/phase_status.md)

## Definitions
- Skeleton: minimal contracts and boundaries with no implementation.
- MVP: minimal working flow that proves core value in one context.
- Future: any capability not required for the skeleton or MVP.

## Phases

### Phase 0: Docs and governance baseline
Outcomes
- Docs index, roadmap, minimal specs, and audit status.

Non-goals
- No application code.
- No APIs, UI, or integrations.

Dependencies
- Vision doc.

Definition of Done
- Roadmap and specs exist and are linked in docs/index.md.
- Audit shows blockers resolved.
- Baseline commands are documented.

Stop conditions
- Conflicting authority or missing vision reference.

### Phase 1: Domain contracts skeleton
Outcomes
- Core entities, value objects, and invariants documented.
- Minimal IAM, time reservation, and conflict detection specs.

Non-goals
- No scheduling heuristics.
- No persistence or framework bindings.

Dependencies
- Phase 0 done.

Definition of Done
- Specs listed in docs/specs/index.md are complete and cross linked.
- Open questions captured without assumptions.

Stop conditions
- Missing or ambiguous identity or organization boundaries.

### Phase 2: Application ports and adapters skeleton
Outcomes
- Command and query ports documented for core domains.
- Adapter boundaries documented without implementation.

Non-goals
- No framework selection or wiring.
- No network protocols or APIs.

Dependencies
- Phase 1 done.

Definition of Done
- Ports are documented in specs with inputs and outputs.
- No code changes required.

Stop conditions
- Ports require undefined data model elements.

### Phase 3: Persistence skeleton
Outcomes
- Storage contracts defined as interfaces only.
- Minimal storage invariants documented.

Non-goals
- No database selection.
- No migrations or schemas.

Dependencies
- Phase 2 done.

Definition of Done
- Persistence contracts are defined in specs or a dedicated storage spec.
- No persistence implementation exists.

Stop conditions
- Any storage contract conflicts with domain invariants.

### Phase 4: API and HTTP framework wiring (future)
Outcomes
- Candidate framework selection documented.

Non-goals
- No API implementation.

Dependencies
- Phase 3 done.

Definition of Done
- Decision recorded for framework candidate only.

Stop conditions
- Baseline tests are not green.

### Phase 5+: Intelligence, finance, marketplace, offline, BI, integrations (future)
Outcomes
- Capability specs only, no implementation.

Non-goals
- No scoring heuristics, pricing logic, or external integrations.

Dependencies
- Phase 4 done.

Definition of Done
- Each capability has a minimal spec or a declared placeholder section.

Stop conditions
- Any dependency on missing core contracts.

## Vision to roadmap mapping
| Vision area | Roadmap phase | Spec or placeholder |
| --- | --- | --- |
| Identity and access management | Phase 1 | docs/specs/iam_minimal.md |
| Time and reservation engine | Phase 1 | docs/specs/time_reservation_engine.md |
| Conflict detection and resolution | Phase 1 | docs/specs/conflict_engine_minimal.md |
| Execution and timesheet workflow | Phase 5+ | [FUTURE: Execution workflow](#future-execution-and-timesheet-workflow) |
| Resource matching intelligence | Phase 5+ | [FUTURE: Resource matching](#future-resource-matching-intelligence) |
| Financial intelligence | Phase 5+ | [FUTURE: Financial intelligence](#future-financial-intelligence) |
| Automation and intelligence layer | Phase 5+ | [FUTURE: Automation layer](#future-automation-and-intelligence-layer) |
| Marketplace and trust | Phase 5+ | [FUTURE: Marketplace and trust](#future-marketplace-and-trust) |
| Notifications and communication | Phase 5+ | [FUTURE: Notifications](#future-notifications-and-communication) |
| Analytics and BI | Phase 5+ | [FUTURE: Analytics and-bi](#future-analytics-and-bi) |
| Mobile first and offline | Phase 5+ | [FUTURE: Mobile offline](#future-mobile-first-and-offline) |
| Security and compliance | Phase 5+ | [FUTURE: Security and compliance](#future-security-and-compliance) |
| Integrations and ecosystem | Phase 5+ | [FUTURE: Integrations](#future-integrations-and-ecosystem) |

## FUTURE: Execution and timesheet workflow
Placeholder for minimal execution workflow spec.

## FUTURE: Resource matching intelligence
Placeholder for minimal matching contract.

## FUTURE: Financial intelligence
Placeholder for financial tracking contract.

## FUTURE: Automation and intelligence layer
Placeholder for automation rules contract.

## FUTURE: Marketplace and trust
Placeholder for marketplace and trust contract.

## FUTURE: Notifications and communication
Placeholder for notification channels contract.

## FUTURE: Analytics and BI
Placeholder for analytics and BI contract.

## FUTURE: Mobile first and offline
Placeholder for mobile and offline sync contract.

## FUTURE: Security and compliance
Placeholder for security and compliance contract.

## FUTURE: Integrations and ecosystem
Placeholder for integrations and ecosystem contract.
