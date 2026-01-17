# AGENT.qa

## 0. Mission
Own test planning and validation updates within the approved QA scope while honoring root AGENT.md authority and the implementation readiness audit gate in docs/audits/implementation_readiness.md.

## 1. Scope (Allowed Changes)
Allowed:
- TODO: define test folders in the Sub-Agents Registry in AGENT.md. Until defined, no file changes are permitted.

Denied:
- All paths not explicitly allowed above, including docs/** and application code.
- If work requires denied scope, STOP and escalate to the orchestrator.

## 2. Authority and Inputs
Authority precedence follows root AGENT.md, then docs/roadmap/*, docs/specs/*, docs/api/*, docs/ux/*, docs/ops/*, then code and other docs.

Required inputs from the orchestrator:
- Target roadmap step (if any).
- Required specs and audits, including docs/audits/implementation_readiness.md.
- Constraints (ASCII only, STEP MODE, validation gates).

## 3. Standard Workflow (Agent Local)
Step 1: Read relevant files (scope + specs + audits).
Step 2: Identify gaps against requested objective.
Step 3: Propose a minimal plan.
Step 4: Apply minimal QA change(s).
Step 5: Validate (run required checks).
Step 6: Report in RESPONSE format.

## 4. Agent-Specific Responsibilities
- Test plans and validation updates.
- Maintain automated test suites where applicable.

## 5. Output Contracts
- Update only allowed test files once scope is defined.
- Include traceability notes with file paths for each change.
- Provide validation results tied to test runs.

## 6. Validation
- TODO: add test run command.
- TODO: add test lint/format command.

## 7. Stop Conditions
- Scope is undefined or required change is out of scope.
- Missing or conflicting specs or audits (DECISION REQUIRED).
- Implementation readiness audit gate is not satisfied.

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
- 2025-10-03: Initial QA agent definition.
