# Base UX - RH and staff planning app (Skello inspired)

## Goal
Provide a mobile-first, fast, and accessible UX baseline for a 2026 SaaS HR and staff
planning app. The experience must be intuitive, ergonomic, and customizable to
improve adoption and productivity while enforcing labor rules and collective
agreements.

This document is formatted as design documentation and can be used directly in
Figma or Framer.

## User journeys (Web and Mobile)

### Web journey (Manager)
1. Login (secure). First login triggers initial setup (site type, collective
   agreement, company rules) so legal constraints are applied immediately.
2. Dashboard shows key KPIs and pending tasks (leave approvals, overtime alerts).
3. Planning module to build weekly schedules with a Smart Planner that assigns
   the right people to the right shifts while respecting constraints.
4. Real-time compliance checks highlight violations (overtime, missing rest).
5. Publish planning and notify employees (mobile push, email, SMS).
6. Requests module: approve or reject leave and absence requests; balances update
   automatically. Shift swap requests are reviewed and approved here.
7. Time tracking (badgeuse): compare planned vs actual hours, validate time
   sheets, and handle corrections.
8. Reports: analyze hours, overtime, labor costs, and export to payroll.

### Mobile journey (Employee)
1. Login (mobile-first, essential info first).
2. Home shows personal schedule (week or day) and real-time updates.
3. Request leave or absence quickly; track status (pending/approved/denied) and
   see updated balances.
4. Request a shift swap or replacement from the mobile app.
5. Check-in / check-out with a large thumb-friendly button and optional PIN or
   biometrics. Optional geolocation to verify on-site clocking.
6. Personal space: profile, contract, and documents (pay slips, certificates).
7. Notifications: shift reminders, new documents, request status updates, company
   announcements.

## Key screens structure

### Login
- Clean, welcoming screen with email and password fields and a primary CTA.
- Forgot password flow and optional SSO or biometric login on mobile.
- Optional quick onboarding after first login.

### Dashboard
- Tile-based overview: weekly summary, pending requests, compliance alerts.
- Quick actions to relevant modules.
- Simple charts and clear typography for fast scanning.

### Planning (Calendar)
- Web: weekly grid (days as columns, employees as rows).
- Mobile: simplified list or day view with quick navigation.
- Shifts as colored blocks with hours, role, and duration.
- Absences shown as distinct blocks (gray or patterned).
- Drag/drop edits, resize for duration, double click for details.
- Smart Planner suggestions and ability to duplicate a week.
- Compliance alerts in real-time (visual highlights and messages).
- Publish button with notifications to staff.

### Employees (Directory and Profile)
- Directory list with avatar, role, and status; search and filters.
- Profile details: personal info, contract, working time rules, balances.
- Documents section with signed contracts and admin documents.
- Roles and permissions management.

### Time tracking (Badgeuse and time sheet review)
- Employee clock-in screen: large button, minimal UI, offline support.
- Manager review table: planned vs actual, deviations, validation status.
- Corrections supported with audit trail.

### Requests (Leave, absence, replacements)
- Request list with status, type, dates, and actions.
- Detail view includes balances and replacement info.
- Manager can approve or reject, triggers notifications and planning updates.

### Reports and analytics
- Hours report: planned vs actual, overtime, absences by employee and period.
- Payroll export: variables of pay ready for payroll tools.
- KPI dashboards: absenteeism, labor cost, productivity indicators.
- Compliance summary: highlight any rule violations.

### Settings and administration
- Company profile, timezone, week settings, holiday calendar.
- Planning rules and collective agreement settings.
- Roles, permissions, and user invitations.
- Branding, theme (light/dark), and notification preferences.
- Integrations (payroll, SSO, HRIS).

## Mobile app structure
- Bottom navigation with 4 tabs: Planning, Team, Requests, Profile.
- Thumb-friendly targets and simple layouts.
- Pull-to-refresh and swipe actions for quick approvals.

## Design system (style guide)

### Color palette
- Neutral backgrounds: #F6F6F8
- Borders and separators: #C0C3D1
- Primary text: #52565C
- Primary brand: #2536CF
- Alert or destructive: #CF3024
- Secondary colors for status (success, warning) with accessible contrast.

### Typography
- Sans-serif font (Inter, Roboto, or Source Sans Pro).
- Base text: 16px desktop, 14px mobile.
- Titles: H1 32px bold, H2 24px semi-bold, H3 20px.
- Line height ~1.5 for readability.

### Components
- Buttons: primary, secondary, and icon buttons with hover/pressed states.
- Inputs: labels, focus state (blue border), error messages in red.
- Navigation: sidebar for desktop, bottom tabs for mobile.
- Cards: white background, subtle shadow, rounded corners.
- Tables: zebra stripes, clear headers, responsive transformations on mobile.
- Modals: centered dialog with primary and secondary actions.
- Badges: status pills (Pending, Approved, Rejected).
- Tooltips: compact and accessible.

### Accessibility
- Contrast >= 4.5:1 for text.
- Visible focus outline for keyboard navigation.
- Touch targets >= 44px on mobile.

## Micro-interactions
- Smooth transitions between screens (200-300ms).
- Hover and focus feedback on desktop.
- Action feedback: button morph to check after publish or approve.
- Skeleton loading for data-heavy views (planning, reports).
- Empty states with clear guidance.
- Mobile gestures: pull-to-refresh, swipe actions.
- Planning drag-and-drop with live preview and snap animation.

## Modular architecture and roles
- Modules (Planning, Badgeuse, Requests, Reports) can be enabled per customer.
- Navigation adapts to enabled modules.
- Role-based UI (Admin, Manager, Employee) shows only relevant features.
- Responsive and mobile-first layout with progressive enhancement.
- Compliance rules integrated into planning and requests flows.
- Offline or poor network handling with queued actions and sync status.

## References
- Skello product inspiration: https://www.skello.io/
- Example UX sources and market research captured in project notes.
