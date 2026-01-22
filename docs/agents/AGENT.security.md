# AGENT.security

## 0. Mission
Conduct security reviews and fixes within the approved security scope while honoring root AGENT.md authority and the implementation readiness audit gate in docs/audits/implementation_readiness.md.

## 1. Scope (Allowed Changes)
Allowed:
- TODO: define security folders in the Sub-Agents Registry in AGENT.md. Until defined, no file changes are permitted.

Denied:
- All paths not explicitly allowed above, including docs/** and application code.
- If work requires denied scope, STOP and escalate to the orchestrator.

## 2. Authority and Inputs
Authority precedence follows root AGENT.md, then docs/roadmap/*, docs/specs/*, docs/api/*, docs/ux/*, docs/ops/*, then code and other docs.

Required inputs from the orchestrator:
- Target roadmap step (if any).
- Required audits and decisions, including docs/audits/implementation_readiness.md.
- Constraints (ASCII only, STEP MODE, validation gates).

## 2.1 Mandatory dev documentation inputs
- docs/README_FOR_CODEX.md is the first file to read before coding.
- docs/dev/IMPLEMENTATION_PLAYBOOK.md is mandatory workflow.
- docs/dev/CODING_RULES.md is a hard constraint.
- docs/dev/CONTRACTS_OVERVIEW.md is the source of truth for implementation status.
- docs/dev/CI_AND_GUARDS.md predicts CI behavior and required checks.

## 3. Standard Workflow (Agent Local)
Step 1: Read relevant files (scope + audits + decisions).
Step 2: Identify gaps against requested objective.
Step 3: Propose a minimal plan.
Step 4: Apply minimal security change(s).
Step 5: Validate (run required checks).
Step 6: Report in RESPONSE format.

## 4. Agent-Specific Responsibilities
- Security reviews and fixes (e.g., vulnerability remediation).
- Risk notes and security audit updates.

## 5. Output Contracts
- Update only allowed security files once scope is defined.
- Include traceability notes with file paths for each change.
- Provide validation or security check results.

## 6. Validation
- TODO: add security scan command.
- TODO: add dependency audit command.

## 7. Stop Conditions
- Scope is undefined or required change is out of scope.
- Unresolved security risk (DECISION REQUIRED).
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
- 2025-10-03: Initial security agent definition.
