# Spec: IAM minimal

## Purpose
Define minimal identity and access model for foundation.

## Non-goals
- SSO, OAuth, or MFA.
- Advanced RBAC policies.
- Audit trail implementation.

## Data model (minimal)
- User
  - id
  - email
  - display_name
- Membership
  - id
  - user_id
  - organization_id
  - role (owner, admin, member)

## Invariants
- User is global; Membership grants access per organization.
- Role must be one of: owner, admin, member.

## Error and edge cases
- Duplicate membership for the same user and organization is invalid.
- Deactivated users cannot create shifts or reservations.

## References
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md
- Roadmap: docs/roadmap/roadmap_v1.md (Foundation step 2)
