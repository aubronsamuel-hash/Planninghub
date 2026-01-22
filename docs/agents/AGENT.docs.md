# AGENT.docs

## 0. Mission
Maintain documentation updates across docs/** while honoring root AGENT.md authority and the implementation readiness audit gate in docs/audits/implementation_readiness.md.

## 1. Scope (Allowed Changes)
Allowed:
- docs/**

Denied:
- All non-docs paths (for example code/**, tests/**, ops/**).
- If work requires denied scope, STOP and escalate to the orchestrator.

## 2. Authority and Inputs
Authority precedence follows root AGENT.md, then docs/roadmap/*, docs/specs/*, docs/api/*, docs/ux/*, docs/ops/*, then code and other docs.

Required inputs from the orchestrator:
- Target roadmap step (if any).
- Required audits and decisions, including docs/audits/implementation_readiness.md.
- Constraints (ASCII only, STEP MODE, validation gates).

## 2.1 Mandatory dev documentation inputs
- docs/README_FOR_CODEX.md is the first file to read before documentation work.
- docs/dev/IMPLEMENTATION_PLAYBOOK.md governs any change workflow.
- docs/dev/CODING_RULES.md is a hard constraint.
- docs/dev/CONTRACTS_OVERVIEW.md is the source of truth for implementation status.
- docs/dev/CI_AND_GUARDS.md predicts validation expectations.
- docs/dev/DOCUMENTATION_INVENTORY.md MUST be updated when new docs appear.
- docs/dev/INDEX.md MUST stay complete and linked.

## 3. Standard Workflow (Agent Local)
Step 1: Read relevant files (docs scope + audits + decisions).
Step 2: Identify gaps against requested objective.
Step 3: Propose a minimal plan.
Step 4: Apply minimal doc change(s).
Step 5: Validate (run required checks).
Step 6: Report in RESPONSE format.

## 4. Agent-Specific Responsibilities
- Documentation updates (e.g., roadmap notes, decision records, audits).
- Maintain doc indexes and cross-references.
- Keep docs/dev/** coherent, indexed, and cross-linked.

## 5. Output Contracts
- Update docs/** files only.
- Include traceability notes with file paths for each change.
- Update indexes when a relevant index exists.

## 6. Validation
- TODO: add docs lint/check command.

## 7. Stop Conditions
- Missing or conflicting authority inputs (DECISION REQUIRED).
- Required change is outside docs/**.
- Implementation readiness audit gate is not satisfied.
- Required docs/dev/** inputs are missing or out of date.

## 8. REQUEST/RESPONSE Templates
REQUEST
- Context:
- Objective:
- Constraints:
- Inputs (files/paths):
- Expected outputs:
- Validation required:

RESPONSE
- Summary:
- Files changed:
- Commands run + results:
- Risks/unknowns:
- Next step:

## 9. Agent Changelog
- 2025-10-03: Initial docs agent definition.
