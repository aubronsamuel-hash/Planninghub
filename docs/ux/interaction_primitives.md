# Interaction Primitives

This document defines read-only, generic UX primitives.
No editing, drag, or data mutation is allowed here.

## Timeline grid
- A time-based grid used to align visual items.
- Read-only reference structure for positioning.

## Resource row
- A labeled row representing a single resource.
- Read-only label and row area aligned to the timeline grid.

## Block (shift or reservation visualization)
- A visual block placed within a resource row.
- Represents a time span only.
- Read-only display of start and end boundaries.

## Hover, select, focus
- Hover: transient highlight while pointer is over an element.
- Select: persistent highlight indicating current selection.
- Focus: keyboard focus indication on a single element.

## Tooltip and side panel
- Tooltip: small read-only summary attached to a hovered or focused element.
- Side panel: read-only details panel for a selected element.

## Loading, empty, error states
- Loading: indicates data is being fetched.
- Empty: indicates no items are available for the current view.
- Error: indicates the view failed to load data.
