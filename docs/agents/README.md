# Agents

Agents are specialized collaborators that operate within defined scopes and follow the root orchestrator.

- The authoritative orchestrator is AGENT.md at the repository root.
- Agents are registered and updated in the Sub-Agents Registry section of AGENT.md.
- Any agent change must be logged in the AGENT CHANGELOG.

Primary index: docs/agents/index.md.

Available agents:
- [agent_docs_governance](agent_docs_governance.md): Governance docs, audits, and indexes.
- [agent_backend](agent_backend.md): Backend changes and services.
- [agent_frontend](agent_frontend.md): UI and UX implementation.
- [agent_data_model](agent_data_model.md): Data models and schemas.
- [agent_ops_ci](agent_ops_ci.md): CI, infra, and operational scripts.

Legacy agents:
- [AGENT.backend](AGENT.backend.md): Backend changes and services.
- [AGENT.frontend](AGENT.frontend.md): UI and UX implementation.
- [AGENT.docs](AGENT.docs.md): Documentation updates under docs/**.
- [AGENT.devops](AGENT.devops.md): CI/CD, infra, and operational scripts.
- [AGENT.qa](AGENT.qa.md): Test planning and validation.
- [AGENT.data](AGENT.data.md): Data pipelines and models.
- [AGENT.security](AGENT.security.md): Security reviews and fixes.

If an agent needs scope changes or new responsibilities, update AGENT.md and record the change in the changelog.

## Shared rules for all agents
- No agent may write code without reading docs/README_FOR_CODEX.md first.
- No agent may bypass docs/dev/IMPLEMENTATION_PLAYBOOK.md.
- If docs/dev/** conflicts with a higher authority source, a decision document in docs/decisions/ is REQUIRED.
- Every agent MUST declare which docs/dev/** files it consumes and which paths it may modify.
- Any agent MUST refuse to act if required documentation is missing or out of date.
