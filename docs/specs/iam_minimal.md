# Spec: IAM minimal

## Purpose
Define the minimal identity and access model required for the foundation skeleton.

## Scope
- Users and organization memberships.
- Role assignment at the membership level.

## Non-scope
- SSO, OAuth, MFA.
- Advanced RBAC policies or audit trail implementation.

## Core concepts and glossary
- User: a global identity.
- Organization: a tenant boundary for data and access.
- Membership: a link between a user and an organization.
- Role: access level within an organization.

## Data model (conceptual)
- User
  - id
  - email
  - display_name
  - status (active, inactive)
- Organization
  - id
  - name
- Membership
  - id
  - user_id
  - organization_id
  - role (owner, admin, member)

## Commands and queries (ports)
- CreateUser(input: email, display_name) -> User
- DeactivateUser(input: user_id) -> User
- CreateOrganization(input: name) -> Organization
- AddMembership(input: user_id, organization_id, role) -> Membership
- ListMemberships(input: user_id or organization_id) -> Membership[]

## Invariants
- User is global; access is granted via Memberships.
- A user MUST NOT have more than one membership for the same organization.
- Role MUST be one of: owner, admin, member.
- Inactive users MUST NOT create reservations.

## Error taxonomy
- NotFound: user or organization does not exist.
- Conflict: duplicate membership or email.
- Forbidden: action not allowed for role.

## Open questions
- Do we need a separate workspace concept beyond organization?
- Is role granularity sufficient for the first MVP?

## Traceability
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md (Identity and access management)
- Roadmap: docs/roadmap/roadmap_v1.md (Phase 1)
