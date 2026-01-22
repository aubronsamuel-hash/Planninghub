# PlanningHub UI skeleton

This folder hosts the minimal frontend skeleton for PlanningHub. It is static HTML and CSS
with no business logic or API calls.

## Structure
- login.html: login screen skeleton.
- dashboard.html: manager planning dashboard skeleton.
- styles.css: shared styling.

## Integration notes
- Data is placeholder only. No authentication or persistence is implemented.
- UI blocks are prepared to bind to existing ports:
  - Identity ports (users, organizations, memberships).
  - Time reservation ports (reservations).
  - Conflict ports (conflicts).
- Future adapters should map data into the UI without adding business logic.

## Validation
- Manual review against docs/ux/base_ux_rh_planning.md.
