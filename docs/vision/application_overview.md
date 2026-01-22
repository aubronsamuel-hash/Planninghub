# Application Overview

## Purpose
This document explains what the PlanningHub application does, using the
canonical terms and evidence already present in the repository. It is a
high level overview and does not replace specs.

## Product intent (summary)
PlanningHub is a planning system centered on time, assignment, and value.
It manages Reservations and Shifts so Organizations can coordinate work
and detect Conflicts early.

## Core domain objects (glossary aligned)
- Organization: owns scoped data and access for planning.
- User: global identity that can join an Organization via Membership.
- Membership: links a User to an Organization with a role.
- Project: container for Missions and planning context.
- Site: location descriptor for Missions and Shifts.
- Mission: unit of work tied to a Project and optional Site.
- Resource: person or asset assigned to a Reservation or Shift.
- Reservation: time interval that is the source of truth for availability.
- Shift: scheduled execution unit for a Mission and Reservation.
- Conflict: overlap or rule violation tied to a Reservation.

## Primary workflow (minimal)
1) Create an Organization and Users, then link them with Membership.
2) Define Projects and Sites as planning context.
3) Define Missions for the work to be scheduled.
4) Create Reservations for the required time intervals.
5) Assign Resources to Reservations and create Shifts for execution.
6) Detect and resolve Conflicts as they appear.

## Architecture placement (repo aligned)
- Domain: entities and rules for Organization, Mission, Reservation, Shift.
- Application: Ports and handlers that expose planning use cases.
- Adapters: IO translation for CLI, HTTP, and persistence ports.
- Infra: configuration and wiring between adapters and core layers.

## Evidence pointers
- Vision: docs/Planning_hub_architecture_vision_produit_v_1.md
- Glossary: docs/glossary/domain_terms.md
- Core domain model: docs/specs/core_domain_model.md
- IAM: docs/specs/iam_minimal.md
- Reservation engine: docs/specs/time_reservation_engine.md
- Conflict engine: docs/specs/conflict_engine_minimal.md
- Ports and adapters: docs/specs/ports_and_adapters_contracts.md
- Hexagonal architecture: docs/specs/architecture/hexagonal_architecture_contract.md
