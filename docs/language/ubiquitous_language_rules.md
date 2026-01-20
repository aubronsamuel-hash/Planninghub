# Ubiquitous Language Enforcement Rules

## 1. Purpose
- Enforce consistent use of domain terms to keep specs and naming aligned.
- Glossary reference: docs/glossary/domain_terms.md.
- Canonical glossary in specs: docs/specs/00_glossary.md.

## 2. Authoritative Terms
- Glossary terms are authoritative for domain terminology.
- Case sensitivity: UNKNOWN (no explicit rule documented).
- Singular/plural rules: UNKNOWN (no explicit rule documented).

## 3. Allowed Usage Rules
- Glossary terms defined in docs/specs/00_glossary.md are canonical terms used across foundation specs.
- Term usage rules for code identifiers are UNKNOWN (not documented).

## 4. Forbidden Patterns
- Synonyms for existing domain terms: UNKNOWN (no documented prohibition).
- Overloaded terms: UNKNOWN (no documented prohibition).
- Contextual renaming in adapters: UNKNOWN (no documented prohibition).

## 5. Handling Ambiguity
- If term usage is ambiguous or conflicting, stop and create a decision entry in docs/decisions using the AGENT.md template.
- Record the ambiguity and the required decision in the decision entry.

## 6. Enforcement Scope
- Applies to docs, specs, roadmap, and code identifiers (naming only, not behavior).
- Out of scope: code behavior. Comments and other text not specified are UNKNOWN.
