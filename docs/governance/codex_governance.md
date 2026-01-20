# Codex governance

## Role of Codex
Codex MUST operate inside the repository and follow AGENT.md as the primary process authority. Codex documents and enforces the governance rules that keep work traceable and safe. See docs/agents/agent_docs_governance.md for the documentation scope and stop conditions.

## Step mode
Codex MUST operate in STEP MODE:
- Read relevant files before acting.
- Make explicit, minimal changes.
- Validate against defined gates before declaring completion.

## No autopilot
Codex MUST NOT perform actions without explicit scope and evidence. If a decision is required, Codex MUST stop and record a decision entry using the template in AGENT.md.

## Read vs write scope
- Read scope: any files needed to establish evidence.
- Write scope: only the paths allowed by the active agent scope (for documentation tasks, docs/** plus AGENT.md and README.md).

## Validation gates
Codex MUST NOT skip validation gates defined in AGENT.md. If a gate is not applicable or cannot run, it MUST be recorded explicitly.

## Stop conditions
Codex MUST stop when any of the following occur:
- Conflicting authority or unclear source of truth.
- Missing index for a touched documentation file.
- Unclear requirements that require a decision.
