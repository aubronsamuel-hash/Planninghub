# Architecture Release Notes

## 1. Purpose
- These notes are derived from ADRs in docs/architecture/decisions only.

## 2. Chronological Summary
- ADR-0001: Ports and adapters architecture
  Impact:
  - PlanningHub uses a ports and adapters (hexagonal) architecture with inward dependencies.
  - Port definitions live under planninghub/application/ports, and adapter contracts and implementations are documented under docs/specs/adapters and planninghub/adapters.
  - Application, domain, and infrastructure layers are separated in documentation and code layout.
- ADR-0002: Invariant enforcement boundaries
  Impact:
  - Invariants are defined in domain specs and owned by the application core.
  - Adapters enforce only invariants defined in domain specs.
  - Invariants are listed in docs/specs/18_invariants_minimal.md.
- ADR-0003: Documentation authority and conflict resolution
  Impact:
  - Documentation conflicts are resolved by the documented authority order.
  - Conflicts require a decision entry in docs/decisions using the AGENT.md template.
- ADR-0004: Codex operating mode step mode
  Impact:
  - Codex operates in step mode only.
  - Operational guidance in AGENT.md enforces step mode for repository work.

## 3. Current Architecture Snapshot
- Ports and adapters (hexagonal) architecture with inward dependencies.
- Port definitions live under planninghub/application/ports.
- Adapter contracts are documented under docs/specs/adapters and implementations live under planninghub/adapters.
- Application, domain, and infrastructure layers are separated in documentation and code layout.
- Invariants are defined in domain specs and owned by the application core.
- Adapters enforce only invariants defined in domain specs.
- Documentation conflicts are resolved by the documented authority order with decisions in docs/decisions.
- Codex operates in step mode only for repository work.
