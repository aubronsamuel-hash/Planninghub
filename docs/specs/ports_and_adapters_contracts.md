# Ports and Adapters Contracts (Locked)

## Purpose
Lock the current ports and adapters contracts based on the existing repository
state. This document is descriptive and must not introduce new behavior.

## Scope and evidence
- Application ports and handlers in planninghub/application.
- Adapters in planninghub/adapters and planninghub/infra.
- DTOs in planninghub/application/dtos and planninghub/adapters/http.

## Ports

### Inbound application ports

#### EvaluateIncomingReservationCommand (inbound command)
- Name: EvaluateIncomingReservationCommand / EvaluateIncomingReservationResponse
- Responsibility:
  - Evaluate an incoming reservation for conflicts and return a resolution
    proposal and outcome if a conflict exists.
- Input DTO (fields + types):
  - organization_id: str
  - reservation: Reservation (domain entity with fields)
    - id: str
    - organization_id: str
    - resource_id: str | None
    - starts_at_utc: datetime
    - ends_at_utc: datetime
    - timezone: str
    - economic_value: float | None
    - status: ReservationStatus
- Output DTO (fields + types):
  - reservation_id: str
  - conflict: bool
  - proposal: ResolutionProposal | None
  - outcome: ResolutionOutcome | None
- Error contract:
  - Propagates ValueError raised by domain services or adapters, if any.
- Determinism guarantees:
  - Deterministic for a given reservation, organization_id, repository state,
    and strategy list ordering.
- MUST NOT:
  - Persist data.
  - Select infrastructure or perform I/O.
  - Skip conflict evaluation when a strategy list is provided.

#### CreateUserPort
- Name: CreateUserPort
- Responsibility: Create a user in the identity boundary.
- Input DTO (fields + types):
  - CreateUserRequest
    - email: str
    - display_name: str
- Output DTO (fields + types):
  - CreateUserResponse
    - user: UserDTO (id: str, email: str, display_name: str, status: str)
- Error contract:
  - Propagates ValueError from the persistence adapter if validation fails.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Apply business rules beyond those enforced by the persistence port.
  - Access infrastructure directly.

#### DeactivateUserPort
- Name: DeactivateUserPort
- Responsibility: Deactivate a user by id.
- Input DTO (fields + types):
  - DeactivateUserRequest
    - user_id: str
- Output DTO (fields + types):
  - DeactivateUserResponse
    - user: UserDTO
- Error contract:
  - Propagates KeyError or ValueError from the persistence adapter.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Create or delete users.
  - Perform I/O directly.

#### CreateOrganizationPort
- Name: CreateOrganizationPort
- Responsibility: Create an organization.
- Input DTO (fields + types):
  - CreateOrganizationRequest
    - name: str
- Output DTO (fields + types):
  - CreateOrganizationResponse
    - organization: OrganizationDTO (id: str, name: str)
- Error contract:
  - Propagates ValueError from the persistence adapter if validation fails.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Add memberships or users as a side effect.
  - Perform I/O directly.

#### AddMembershipPort
- Name: AddMembershipPort
- Responsibility: Add a membership for a user in an organization.
- Input DTO (fields + types):
  - AddMembershipRequest
    - user_id: str
    - organization_id: str
    - role: str
- Output DTO (fields + types):
  - AddMembershipResponse
    - membership: MembershipDTO
- Error contract:
  - Raises ValueError when organization_id is empty.
  - Raises ValueError when a duplicate membership exists for user_id and
    organization_id.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Assign roles outside the request.
  - Skip duplicate membership checks.

#### ListMembershipsPort
- Name: ListMembershipsPort
- Responsibility: List memberships filtered by user_id and/or organization_id.
- Input DTO (fields + types):
  - ListMembershipsRequest
    - user_id: str | None
    - organization_id: str | None
- Output DTO (fields + types):
  - ListMembershipsResponse
    - memberships: list[MembershipDTO]
- Error contract:
  - Raises ValueError if user_id or organization_id is provided as an empty
    string.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Mutate memberships.
  - Apply additional filtering not in the request.

#### CreateReservationPort
- Name: CreateReservationPort
- Responsibility: Create a reservation.
- Input DTO (fields + types):
  - CreateReservationRequest
    - organization_id: str
    - resource_id: str | None
    - starts_at_utc: datetime
    - ends_at_utc: datetime
    - timezone: str
    - economic_value: float | None
- Output DTO (fields + types):
  - CreateReservationResponse
    - reservation: ReservationDTO
- Error contract:
  - Raises ValueError if organization_id is empty.
  - Raises ValueError if starts_at_utc >= ends_at_utc.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Auto-assign status outside the persistence adapter.
  - Accept invalid time intervals.

#### UpdateReservationPort
- Name: UpdateReservationPort
- Responsibility: Update a reservation with partial fields.
- Input DTO (fields + types):
  - UpdateReservationRequest
    - reservation_id: str
    - starts_at_utc: datetime | None
    - ends_at_utc: datetime | None
    - resource_id: str | None
    - status: str | None
- Output DTO (fields + types):
  - UpdateReservationResponse
    - reservation: ReservationDTO
- Error contract:
  - Raises ValueError if starts_at_utc and ends_at_utc are both provided and
    starts_at_utc >= ends_at_utc.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Alter organization_id or timezone.
  - Bypass interval validation when both timestamps are provided.

#### GetReservationPort
- Name: GetReservationPort
- Responsibility: Fetch a reservation by id.
- Input DTO (fields + types):
  - GetReservationRequest
    - reservation_id: str
- Output DTO (fields + types):
  - GetReservationResponse
    - reservation: ReservationDTO
- Error contract:
  - Propagates KeyError from the persistence adapter when missing.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Mutate the reservation.

#### ListReservationsPort
- Name: ListReservationsPort
- Responsibility: List reservations by organization, optional resource and
  optional time range.
- Input DTO (fields + types):
  - ListReservationsRequest
    - organization_id: str
    - resource_id: str | None
    - time_range: TimeRangeDTO | None
      - start_utc: datetime
      - end_utc: datetime
- Output DTO (fields + types):
  - ListReservationsResponse
    - reservations: list[ReservationDTO]
- Error contract:
  - Raises ValueError if organization_id is empty.
  - Raises ValueError if time_range.start_utc >= time_range.end_utc.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Add implicit filtering beyond request criteria.

#### DetectConflictsPort
- Name: DetectConflictsPort
- Responsibility: Detect conflicts for a reservation within an organization.
- Input DTO (fields + types):
  - DetectConflictsRequest
    - organization_id: str
    - reservation_id: str
- Output DTO (fields + types):
  - DetectConflictsResponse
    - conflicts: list[ConflictDTO]
- Error contract:
  - Raises ValueError if organization_id is empty.
  - Propagates KeyError if reservation_id is unknown in persistence adapter.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Create reservations.
  - Modify conflicts outside the persistence adapter.

#### ListConflictsPort
- Name: ListConflictsPort
- Responsibility: List conflicts for an organization, optional reservation_id.
- Input DTO (fields + types):
  - ListConflictsRequest
    - organization_id: str
    - reservation_id: str | None
- Output DTO (fields + types):
  - ListConflictsResponse
    - conflicts: list[ConflictDTO]
- Error contract:
  - Raises ValueError if organization_id is empty.
  - Raises ValueError if reservation_id is provided as an empty string.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Create conflicts.
  - Apply filters not in the request.

### Outbound persistence ports

#### IdentityPersistencePort
- Responsibility: Persist identity DTOs.
- Methods and DTOs:
  - create_user(CreateUserRequest) -> UserDTO
  - deactivate_user(DeactivateUserRequest) -> UserDTO
  - create_organization(CreateOrganizationRequest) -> OrganizationDTO
  - add_membership(AddMembershipRequest) -> MembershipDTO
  - list_memberships(ListMembershipsRequest) -> list[MembershipDTO]
- Error contract:
  - Propagates ValueError for invalid inputs as enforced by adapter.
  - Propagates KeyError for missing entities (adapter specific).
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Apply non-deterministic ID generation without recording a deterministic
    mapping strategy.
  - Perform network I/O in a persistence adapter without explicit contract
    change.

#### ReservationPersistencePort
- Responsibility: Persist reservation DTOs.
- Methods and DTOs:
  - create_reservation(CreateReservationRequest) -> ReservationDTO
  - update_reservation(UpdateReservationRequest) -> ReservationDTO
  - get_reservation(GetReservationRequest) -> ReservationDTO
  - list_reservations(ListReservationsRequest) -> list[ReservationDTO]
- Error contract:
  - Propagates ValueError for invalid intervals.
  - Propagates KeyError for missing reservations (adapter specific).
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Implicitly modify reservation time ranges.
  - Inject conflicts or status changes outside the request.

#### ConflictPersistencePort
- Responsibility: Persist conflict DTOs.
- Methods and DTOs:
  - detect_conflicts(DetectConflictsRequest) -> list[ConflictDTO]
  - list_conflicts(ListConflictsRequest) -> list[ConflictDTO]
- Error contract:
  - Propagates ValueError for invalid organization_id.
  - Propagates KeyError when referenced reservations are missing.
- Determinism guarantees:
  - Deterministic for a given request and persistence state.
- MUST NOT:
  - Create conflicts unrelated to existing reservations.

### Domain repository ports

#### MembershipRepository
- Responsibility: Persist domain Membership entities for domain services.
- Inputs and outputs:
  - add(membership: Membership) -> None
  - get_by_id(membership_id: str) -> Membership | None
  - list_by_org(organization_id: str) -> list[Membership]
  - find_by_user(organization_id: str, user_id: str) -> list[Membership]
- Error contract:
  - None defined; implementations may return None or raise on missing items.
- Determinism guarantees:
  - Deterministic for a given repository state.
- MUST NOT:
  - Perform conflict detection logic.

#### ReservationRepository
- Responsibility: Persist domain Reservation entities for domain services.
- Inputs and outputs:
  - add(reservation: Reservation) -> None
  - get_by_id(reservation_id: str) -> Reservation | None
  - list_by_org(organization_id: str) -> list[Reservation]
  - list_by_resource(organization_id: str, resource_id: str) -> list[Reservation]
  - list_overlapping(organization_id: str, resource_id: str,
    starts_at_utc: datetime, ends_at_utc: datetime) -> list[Reservation]
- Error contract:
  - None defined; implementations may return None or raise on missing items.
- Determinism guarantees:
  - Deterministic for a given repository state.
- MUST NOT:
  - Apply resolution strategies or business rules outside persistence.

## Handlers
- EvaluateIncomingReservationHandler implements the evaluation command and
  orchestrates conflict detection and resolution strategies.
- Identity handlers implement identity ports:
  CreateUserHandler, DeactivateUserHandler, CreateOrganizationHandler,
  AddMembershipHandler, ListMembershipsHandler.
- Time reservation handlers implement reservation ports:
  CreateReservationHandler, UpdateReservationHandler, GetReservationHandler,
  ListReservationsHandler.
- Conflict handlers implement conflict ports:
  DetectConflictsHandler, ListConflictsHandler.

## Adapters and boundary DTOs

### HTTP adapter
- DTOs:
  - EvaluateIncomingReservationRequestDTO
    - organization_id: str
    - reservation_id: str
    - resource_id: str | None
    - starts_at_utc_iso: str
    - ends_at_utc_iso: str
    - timezone: str
  - EvaluateIncomingReservationResponseDTO
    - reservation_id: str
    - conflict: bool
    - outcome: str | None
    - action: str | None
    - details: dict[str, str] | None
- Mapper determinism:
  - request_dto_to_command parses ISO timestamps using datetime.fromisoformat
    and sets ReservationStatus.ACTIVE with economic_value=None.
  - response_to_response_dto maps outcome and proposal fields directly from the
    application response.

### CLI adapter
- CLI entrypoint creates EvaluateIncomingReservationCommand and calls
  EvaluateIncomingReservationHandler with in-memory repository and a noop
  resolution strategy.

### Persistence adapters
- StubPersistenceAdapter implements the persistence ports with NotImplemented
  methods for skeleton usage.
- InMemoryPersistenceAdapter implements IdentityPersistencePort,
  ReservationPersistencePort, and ConflictPersistencePort with deterministic
  id generation using incrementing counters per prefix.
  - Conflict detection emits a severity of "high" and reason
    "overlap:<other-id>" for overlapping reservations with the same resource
    within the organization.

### Domain in-memory repositories
- InMemoryMembershipRepository implements MembershipRepository with deterministic
  in-memory storage and sorted outputs by id.
- InMemoryReservationRepository implements ReservationRepository with sorted
  outputs and overlap filtering based on UTC timestamps.

## Locked contracts
The following contracts are now frozen and MUST NOT be changed without an
explicit decision note in docs/decisions:
- Application port interfaces and DTOs in planninghub/application/ports and
  planninghub/application/dtos.
- Domain repository ports in planninghub/domain/repositories.
- HTTP adapter DTOs and mapper behavior for reservation evaluation.
- Persistence adapter behavior for the in-memory adapter (deterministic ids and
  conflict severity/reason defaults).
