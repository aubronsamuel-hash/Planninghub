# Spec: Identity ports (minimal)

## Purpose
Define deterministic application ports for identity and access boundaries without selecting any infrastructure.

## Responsibilities
- Create and update core identity records.
- Expose query ports for identity lookups within organization scope.
- Surface authorization boundaries via role-scoped operations.

## Inputs / Outputs (data shapes, not code)
### CreateUser
Input
- email
- display_name

Output: User
- id
- email
- display_name
- status (active, inactive)

### DeactivateUser
Input
- user_id

Output: User
- id
- email
- display_name
- status

### CreateOrganization
Input
- name

Output: Organization
- id
- name

### AddMembership
Input
- user_id
- organization_id
- role (owner, admin, member)

Output: Membership
- id
- user_id
- organization_id
- role

### ListMemberships
Input
- user_id (optional)
- organization_id (optional)

Output: Membership[]
- id
- user_id
- organization_id
- role

## Invariants (referenced)
- User is global; access is granted via Memberships.
- A user MUST NOT have more than one membership for the same organization.
- Role MUST be one of: owner, admin, member.
- Inactive users MUST NOT create reservations.
Reference: docs/specs/iam_minimal.md, docs/specs/18_invariants_minimal.md.

## Explicit NON-responsibilities
- No SSO, OAuth, MFA, or external identity providers.
- No persistence or storage decisions.
- No API or transport protocol definitions.
- No role-based policy evaluation beyond role membership.

## Traceability
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md (Identity and access management)
- Roadmap: docs/roadmap/roadmap_v1.md (Phase 2)
- Source spec: docs/specs/iam_minimal.md
