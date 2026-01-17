# AGENT - Root Orchestrator

## 0. Purpose
This orchestrator exists to coordinate multiple specialized agents, provide a single source of process truth, and keep work safe and repeatable. It is designed to evolve over time as the repository grows and as agents are refined.

## 1. Global Rules (Non Negotiable)
- ASCII only
- STEP MODE only
- Read files before acting
- Never invent repo structure
- Never skip validation gates
- If unclear -> DECISION REQUIRED

## 2. Authority and Source of Truth
Precedence order (highest to lowest):
1) AGENT.md
2) docs/Planning_hub_architecture_vision_produit_v_1.md (canonical vision doc)
3) docs/roadmap/**
4) docs/specs/**
5) docs/ux/**, docs/api/**, docs/ops/**
6) code (planninghub/**)

Note: If a second copy of the vision doc exists elsewhere, it is non-canonical unless explicitly declared.

Conflict handling:
- If two sources conflict, stop and create or update a decision in docs/decisions.
- If ambiguity blocks progress, record it using the Decision Required template.

## 3. Standard Gated Workflow
Gate A: Baseline green (guards/tests if present)
Gate B: Implementation readiness audit (docs/audits/implementation_readiness.md)
Gate C: Roadmap step mapping
Gate D: Minimal execution
Gate E: Validation + docs update

## 4. Sub-Agents Registry (Updatable)
| Agent ID | Agent file | Scope (folders allowed) | Responsibilities | Inputs | Outputs | Validation | Stop conditions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AGENT.docs_governance | docs/agents/agent_docs_governance.md | docs/** | Governance docs, audits, indexes | vision doc, audits, roadmap | updated docs, logs | doc lint if present | Conflicting authority or missing index |
| AGENT.backend | docs/agents/agent_backend.md | planninghub/** | Backend changes and services | specs, roadmap, audits | code, tests, notes | backend tests if present | Gate failure or unclear spec |
| AGENT.frontend | docs/agents/agent_frontend.md | ui or web folders | UI and UX implementation | specs, ux docs | code, screenshots | frontend tests if present | Gate failure or unclear spec |
| AGENT.data_model | docs/agents/agent_data_model.md | data or models folders | Data models and schemas | specs, audits | model updates | data validation | Missing data sources |
| AGENT.ops_ci | docs/agents/agent_ops_ci.md | ops, ci, infra folders | CI/CD, infra, scripts | ops docs | config changes | pipeline checks | Unsafe change |

### Legacy / deprecated
Deprecated legacy registry files (do not use): docs/agents/AGENT.backend.md, docs/agents/AGENT.frontend.md, docs/agents/AGENT.docs.md, docs/agents/AGENT.devops.md, docs/agents/AGENT.qa.md, docs/agents/AGENT.data.md, docs/agents/AGENT.security.md.

## 5. Agent Invocation Protocol
REQUEST
- Agent ID:
- Scope:
- Objective:
- Inputs:
- Constraints:
- Validation:

RESPONSE
- Summary:
- Files touched:
- Checks run:
- Risks:
- Next step:

## 6. Output Contracts
- Docs change -> index updated (if an index exists)
- Code change -> tests + validation recorded
- Any uncertainty -> audit note or decision entry
- Audits live in docs/audits/

## 7. Update Policy (Agent Evolution)
- Add a new agent by updating the registry table and documenting scope and validation.
- Modify an existing agent by updating its row and noting the change below.
- Log all changes to this section in the AGENT CHANGELOG.

AGENT CHANGELOG
- 2026-01-17: Updated authority order, clarified canonical vision note, and normalized the agent registry to the current agent files.

## 8. Quick Start
- TODO: Add build command
- TODO: Add test command
- TODO: Add lint command

## 9. Decision Required Template
Use this template for docs/decisions entries:

# Decision Required: <short title>

Date: YYYY-MM-DD
Status: Proposed | Accepted | Rejected
Owners: <names or roles>

## Context
- What is the uncertainty?

## Options
1) Option A
2) Option B

## Decision
- DECISION REQUIRED

## Rationale
- Why this decision matters

## Consequences
- What changes after the decision
