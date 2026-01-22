# README for Codex

## Project purpose
PlanningHub is an orchestration engine for time-based resources. It focuses on time reservations as the core domain concept and is designed for neutral scheduling and allocation scenarios without an industry-specific assumption.

## Authority order (summary)
Highest to lowest authority:
1) AGENT.md
2) docs/Planning_hub_architecture_vision_produit_v_1.md (canonical vision)
3) docs/roadmap/**
4) docs/specs/**
5) docs/ux/**, docs/api/**, docs/ops/**
6) code under planninghub/**

If sources conflict, a decision document in docs/decisions/ is REQUIRED before code changes.

## Repo structure (high level)
- planninghub/domain/ : domain entities, value objects, repositories, services, use cases
- planninghub/application/ : application ports, handlers, DTOs
- planninghub/adapters/ : CLI, HTTP, persistence, and transport adapters
- planninghub/infra/ : wiring, config, and in-memory infrastructure utilities
- tests/ : automated tests
- docs/ : governance, specs, roadmap, audits, and developer guides

## Golden rules for coding
- You MUST follow the authority order.
- You MUST NOT add or change behavior without an explicit spec update first.
- You MUST NOT introduce new domain terms outside the glossary.
- You MUST NOT add business logic to adapters.
- You MUST keep dependency direction inward (domain is most isolated).
- You MUST update docs/index.md and any relevant index when touching docs.
- You MUST stop and write a decision in docs/decisions/ if sources conflict.

## What requires a spec update
- Any new command, query, port, or DTO surface.
- Any change to domain invariants or conflict logic.
- Any new persistence adapter behavior.

## What requires a decision document
- Any conflict between AGENT.md and other docs.
- Any change to architectural boundaries or package dependency rules.

## Common failure modes to avoid
- Skipping specs and writing code first.
- Adding business logic in adapters or infra.
- Importing application or infra modules from domain modules.
- Changing tests without a matching spec or contract.
- Ignoring traceability or failing to update indexes.

## Documentation entry points
- Documentation inventory: docs/dev/DOCUMENTATION_INVENTORY.md
- Developer index: docs/dev/INDEX.md
