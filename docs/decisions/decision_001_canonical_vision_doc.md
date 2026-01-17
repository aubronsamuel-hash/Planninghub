# Decision 001 - Canonical Vision Document

Date: 2026-01-17
Status: Accepted
Owners: Product / Architecture

## Context
There was ambiguity regarding the canonical location of the PlanningHub product vision document.
Multiple references existed in prompts and documentation, creating a risk of divergence.

## Decision
The canonical and authoritative vision document is:
docs/Planning_hub_architecture_vision_produit_v_1.md

## Rationale
A single canonical source of truth is required to:
- Prevent documentation drift
- Ensure consistent roadmap and specification alignment
- Allow agents and humans to execute safely without sync ambiguity

## Consequences
- All roadmap, specs, and audits must reference the canonical vision document.
- Any other copies of the vision document are non-canonical and must either be removed
  or explicitly marked as informational only.
- No synchronization policy is introduced.
