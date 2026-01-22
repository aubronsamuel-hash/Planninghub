# Spec: Frontend UI skeleton

## Purpose
Define the minimal frontend UI skeleton for PlanningHub. This covers static pages and
layout only, with no business logic or API wiring.

## Scope
- Static HTML and CSS under ui/.
- Screens:
  - Login.
  - Manager planning dashboard (overview and reservation schedule).
- Prepared placeholders for data from existing ports (identity, reservation, conflict).

## Non-goals
- Authentication logic.
- Data persistence or API calls.
- Business rules, validation, or scheduling logic.

## Screens

### Login
- Clean layout with email and password inputs and a primary sign-in action.
- Secondary action for SSO placeholder.
- Helper text notes that identity data will come from ports.

### Planning dashboard (manager)
- Sidebar navigation with links for dashboard, planning, resources, reservations, conflicts.
- KPI cards for reservations, conflicts, memberships, and resources.
- Weekly planning grid with resources as rows and weekdays as columns.
- Conflict alert section tied to conflict data placeholders.

## Component and styling guidance
- Use color palette and typography defined in docs/ux/base_ux_rh_planning.md.
- Buttons: primary and secondary.
- Cards: white background with subtle shadow and rounded corners.
- Table/grid layout for reservations.
- Badges for compact status cues.

## Port alignment placeholders
- Identity ports provide organization and membership context.
- Reservation ports provide reservation list data for the planning grid.
- Conflict ports provide conflict alerts and severity tags.
- UI elements expose data-port attributes for future adapter binding.

## Validation
- Manual review against docs/ux/base_ux_rh_planning.md.
