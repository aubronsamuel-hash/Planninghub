# Implementation playbook

This playbook is mandatory for adding new features.

## Step-by-step workflow

1) Check roadmap
- Read docs/roadmap/roadmap_v1.md.
- Confirm the feature is in scope for the current phase.

2) Check specs
- Read the relevant files under docs/specs/.
- If no spec exists, stop and add one.

3) Add or update spec
- Update docs/specs/ or create a new spec.
- Keep the authority order intact.
- If there is a conflict, write a decision entry first.

4) Add tests
- Add tests that enforce the new or updated contract.
- Place tests in the correct category (see docs/dev/TESTING_GUIDE.md).

5) Implement minimal code
- Make the smallest change needed to satisfy the spec and tests.
- Keep business logic in domain or application layers.
- Keep adapters free of business logic.

6) Update audits and traceability
- Update docs/audits/implementation_readiness.md if status changes.
- Update docs/traceability/spec_to_code_matrix.md and spec_to_tests_matrix.md as needed.
- Update docs/index.md and docs/dev/INDEX.md if new docs are added.

## Evidence that MUST be produced
- Spec update or new spec reference.
- Tests that map directly to the spec.
- Code changes that are limited to the required layers.
- Audit and traceability updates when scope changes.

## What to never skip
- Spec updates.
- Tests for new behavior.
- Traceability updates.
- Decision documentation when authority conflicts.
