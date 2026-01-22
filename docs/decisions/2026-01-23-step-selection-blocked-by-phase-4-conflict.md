# Decision Required: step selection blocked by phase 4 status conflict

Date: 2026-01-23
Status: Accepted
Owners: documentation governance

## Context
- docs/roadmap/roadmap_v1.md defines Phase 4 as future framework wiring only.
- docs/audits/implementation_readiness.md reports Phase 4 as DONE.
- docs/status/phase_status.md previously marked Phase 4 as IN PROGRESS with a decision required.
- This conflict blocks determining the current active phase and the next allowed step.
- Ref: docs/roadmap/roadmap_v1.md#phase-4-api-and-http-framework-wiring-future

## Options
1) Update the roadmap Phase 4 definition to match the audit status.
2) Update the audit and status docs to align with the roadmap future definition.

## Decision
- Phase 4 status is authoritative as DONE per docs/audits/implementation_readiness.md
  (Phase 4 status section). Ref: docs/roadmap/roadmap_v1.md#phase-4-api-and-http-framework-wiring-future

## Rationale
- The phase gating must be authoritative to select the next allowed step.

## Resolution
- docs/status/phase_status.md
- docs/roadmap/roadmap_v1.md
- docs/decisions/2026-01-23-step-selection-blocked-by-phase-4-conflict.md
Ref: docs/roadmap/roadmap_v1.md#phase-4-api-and-http-framework-wiring-future

## Consequences
- Phase 4 status is aligned across roadmap notes and phase status documentation.
- Step selection can proceed using the audit as authoritative evidence.
Ref: docs/roadmap/roadmap_v1.md#phase-4-api-and-http-framework-wiring-future
