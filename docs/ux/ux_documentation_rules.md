# UX Documentation Rules

## Scope
- ASCII only.
- UX documentation lives under docs/ux/.
- Glossary terms are authoritative and MUST be used as written.

## Ubiquitous language alignment
- MUST use glossary terms from docs/glossary/domain_terms.md.
- MUST NOT introduce synonyms for glossary terms.
- If a required term is missing, note it as DECISION REQUIRED.

## Required sections for each UX doc
1) Purpose
2) Context and assumptions
3) Primary actors
4) View structure (read-only unless explicitly labeled)
5) Interaction primitives used (from interaction_primitives.md)
6) States (loading, empty, error)
7) Accessibility notes
8) Open questions or DECISION REQUIRED

## Prohibited content
- MUST NOT define business logic or decision rules.
- MUST NOT describe algorithms or data pipelines.
- MUST NOT include hidden rules or undocumented state transitions.
- MUST NOT describe authorization, security, or backend contracts.

## Traceability notes
- When applicable, link from UX docs to specs or ports.
- Keep links explicit and minimal.
- Do not duplicate spec content.
