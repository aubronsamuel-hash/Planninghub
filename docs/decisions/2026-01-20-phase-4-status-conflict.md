# Decision Required: phase 4 status conflict

Date: 2026-01-20
Status: Accepted
Owners: documentation governance

## Context
- docs/roadmap/roadmap_v1.md defines Phase 4 as future framework wiring only.
- docs/audits/implementation_readiness.md reports Phase 4 as DONE with in-memory adapter guarantees.

## Options
1) Update the roadmap Phase 4 definition to match the audit status.
2) Update the audit Phase 4 status to align with the roadmap future definition.

## Decision
- Phase 4 is AUTHORITATIVELY marked as DONE.
- The source of truth for Phase 4 completion is docs/audits/implementation_readiness.md.
- The roadmap wording for Phase 4 remains unchanged in scope, but its STATUS is considered DONE for this repository.

## Rationale
- The implementation_readiness audit is evidence-based and reflects executed work.
- Governance requires status to be derived from verified audit evidence, not intent wording.
- Leaving Phase 4 as future or in-progress while audit reports DONE blocks deterministic step selection.

## Consequences
- docs/status/phase_status.md MUST mark Phase 4 as DONE.
- docs/roadmap/roadmap_v1.md MAY include a clarification note that Phase 4 is considered DONE per audit evidence.
- Step selection is unblocked for Controlled Forward Progress.
- Any future redefinition of Phase 4 scope requires a new decision file.

## Update 2026-01-24
- Conflict remains unresolved, which blocks identifying the current active phase and
  any next allowed step until a decision is recorded.
Ref: docs/roadmap/roadmap_v1.md#phase-4-api-and-http-framework-wiring-future

Ref: docs/roadmap/roadmap_v1.md#phase-4-api-and-http-framework-wiring-future
Ref: docs/audits/implementation_readiness.md#phase-4
