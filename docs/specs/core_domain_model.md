# Spec: Core domain model

## Purpose
Define the minimal set of core objects required for PlanningHub foundation.

## Non-goals
- Full workflow automation.
- Marketplace or trust features.
- Advanced analytics or AI scoring.

## Data model (minimal)
- Organization
  - id
  - name
  - timezone
- User
  - id
  - email
  - display_name
- Membership
  - id
  - organization_id
  - user_id
  - role (owner, admin, member)
- Project
  - id
  - organization_id
  - name
- Site
  - id
  - organization_id
  - name
  - location_text
- Mission
  - id
  - organization_id
  - project_id
  - site_id
  - name
- Resource
  - id
  - organization_id
  - type (human, asset, service)
  - name
- Shift
  - id
  - mission_id
  - reservation_id
  - status (proposed, accepted, confirmed, in_progress, completed, validated, closed)

## Invariants
- User is global; Membership ties User to Organization.
- Mission belongs to a single Organization via Project or directly by organization_id.
- Shift references exactly one Reservation.
- All entities carry organization_id except User.

## Error and edge cases
- Missing organization_id is invalid for all scoped entities.
- Shift cannot exist without a Reservation reference.

## References
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md
- Roadmap: docs/roadmap/roadmap_v1.md (Foundation step 1)
