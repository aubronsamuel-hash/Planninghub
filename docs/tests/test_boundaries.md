# Test boundaries and forbidden patterns

## Allowed imports
Tests MAY import all layers (domain, application, infra) according to
package boundaries guidance in docs/specs/package_boundaries_and_public_api.md.

## Forbidden imports
No explicit forbidden imports for tests are documented in the repo. UNKNOWN.

## Side effects and determinism
No explicit test governance rules prohibit network, filesystem, nondeterministic
clock access, randomness, or external dependencies. UNKNOWN.

Observed behavior in tests:
- Filesystem usage via tmp_path and sqlite file paths in tests/test_application_wiring.py
  and tests/test_cli_smoke.py.
- In memory adapters and repositories are used across tests for determinism, with
  fixed datetime values in most tests.

## Deterministic practices
Explicit test determinism guidance is not documented. UNKNOWN. Relevant
determinism expectations in specs exist for ports and adapters
(docs/specs/ports_and_adapters_contracts.md,
 docs/specs/persistence_real_adapter_contract.md), but they are not test specific.
