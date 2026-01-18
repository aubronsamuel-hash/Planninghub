# Ports and Adapters Contracts

## 1. Scope and principles
- Scope: application ports in planninghub/application/ports, persistence ports, domain repository ports, and adapter DTOs/mappers in planninghub/adapters plus in-memory implementations in planninghub/adapters and planninghub/infra.
- Determinism: only explicitly implemented ordering and ID generation are treated as deterministic guarantees (for example, in-memory ID counters and sorted in-memory repository listings).
- No business heuristics in adapters: adapters implement ports without adding business logic and preserve data shapes defined by port specs.
- Error contract approach: this document lists only errors explicitly raised in handlers or adapters.

Evidence:
- [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L6-L31]
- [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L49-L287]
- [EVIDENCE:planninghub/infra/repositories_in_memory.py:L11-L92]

## 2. Port inventory (table)
| Port name | Location (path) | Handler(s) using it | Input type(s) | Output type(s) | Errors (if defined) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| EvaluateIncomingReservationCommand/Response | planninghub/application/ports/evaluate_incoming_reservation.py | EvaluateIncomingReservationHandler | EvaluateIncomingReservationCommand (organization_id, Reservation) | EvaluateIncomingReservationResponse | None defined in handler | [EVIDENCE:planninghub/application/ports/evaluate_incoming_reservation.py:L12-L23] [EVIDENCE:planninghub/application/handlers/evaluate_incoming_reservation.py:L18-L42] [EVIDENCE:planninghub/domain/entities.py:L106-L122] |
| CreateUserPort | planninghub/application/ports/identity.py | CreateUserHandler | CreateUserRequest | CreateUserResponse | None defined in handler | [EVIDENCE:planninghub/application/ports/identity.py:L21-L23] [EVIDENCE:planninghub/application/handlers/identity.py:L30-L36] [EVIDENCE:planninghub/application/dtos/identity.py:L31-L40] |
| DeactivateUserPort | planninghub/application/ports/identity.py | DeactivateUserHandler | DeactivateUserRequest | DeactivateUserResponse | None defined in handler | [EVIDENCE:planninghub/application/ports/identity.py:L26-L28] [EVIDENCE:planninghub/application/handlers/identity.py:L39-L45] [EVIDENCE:planninghub/application/dtos/identity.py:L42-L50] |
| CreateOrganizationPort | planninghub/application/ports/identity.py | CreateOrganizationHandler | CreateOrganizationRequest | CreateOrganizationResponse | None defined in handler | [EVIDENCE:planninghub/application/ports/identity.py:L31-L33] [EVIDENCE:planninghub/application/handlers/identity.py:L48-L54] [EVIDENCE:planninghub/application/dtos/identity.py:L52-L60] |
| AddMembershipPort | planninghub/application/ports/identity.py | AddMembershipHandler | AddMembershipRequest | AddMembershipResponse | ValueError on empty organization_id or duplicate membership | [EVIDENCE:planninghub/application/ports/identity.py:L36-L38] [EVIDENCE:planninghub/application/handlers/identity.py:L20-L72] [EVIDENCE:planninghub/application/dtos/identity.py:L62-L72] |
| ListMembershipsPort | planninghub/application/ports/identity.py | ListMembershipsHandler | ListMembershipsRequest | ListMembershipsResponse | ValueError on empty user_id or organization_id when provided | [EVIDENCE:planninghub/application/ports/identity.py:L41-L43] [EVIDENCE:planninghub/application/handlers/identity.py:L25-L83] [EVIDENCE:planninghub/application/dtos/identity.py:L74-L82] |
| CreateReservationPort | planninghub/application/ports/time_reservation.py | CreateReservationHandler | CreateReservationRequest | CreateReservationResponse | ValueError on empty organization_id or invalid interval | [EVIDENCE:planninghub/application/ports/time_reservation.py:L19-L21] [EVIDENCE:planninghub/application/handlers/time_reservation.py:L18-L36] [EVIDENCE:planninghub/application/dtos/time_reservation.py:L28-L40] |
| UpdateReservationPort | planninghub/application/ports/time_reservation.py | UpdateReservationHandler | UpdateReservationRequest | UpdateReservationResponse | ValueError on invalid interval when both timestamps provided | [EVIDENCE:planninghub/application/ports/time_reservation.py:L24-L26] [EVIDENCE:planninghub/application/handlers/time_reservation.py:L39-L47] [EVIDENCE:planninghub/application/dtos/time_reservation.py:L43-L55] |
| GetReservationPort | planninghub/application/ports/time_reservation.py | GetReservationHandler | GetReservationRequest | GetReservationResponse | None defined in handler | [EVIDENCE:planninghub/application/ports/time_reservation.py:L29-L31] [EVIDENCE:planninghub/application/handlers/time_reservation.py:L50-L56] [EVIDENCE:planninghub/application/dtos/time_reservation.py:L57-L65] |
| ListReservationsPort | planninghub/application/ports/time_reservation.py | ListReservationsHandler | ListReservationsRequest | ListReservationsResponse | ValueError on empty organization_id | [EVIDENCE:planninghub/application/ports/time_reservation.py:L34-L36] [EVIDENCE:planninghub/application/handlers/time_reservation.py:L59-L66] [EVIDENCE:planninghub/application/dtos/time_reservation.py:L67-L76] |
| DetectConflictsPort | planninghub/application/ports/conflict.py | DetectConflictsHandler | DetectConflictsRequest | DetectConflictsResponse | ValueError on empty organization_id | [EVIDENCE:planninghub/application/ports/conflict.py:L15-L17] [EVIDENCE:planninghub/application/handlers/conflict.py:L14-L31] [EVIDENCE:planninghub/application/dtos/conflict.py:L19-L28] |
| ListConflictsPort | planninghub/application/ports/conflict.py | ListConflictsHandler | ListConflictsRequest | ListConflictsResponse | ValueError on empty organization_id or empty reservation_id when provided | [EVIDENCE:planninghub/application/ports/conflict.py:L20-L22] [EVIDENCE:planninghub/application/handlers/conflict.py:L14-L42] [EVIDENCE:planninghub/application/dtos/conflict.py:L30-L38] |
| IdentityPersistencePort | planninghub/application/ports/persistence.py | Identity handlers | CreateUserRequest, DeactivateUserRequest, CreateOrganizationRequest, AddMembershipRequest, ListMembershipsRequest | UserDTO, OrganizationDTO, MembershipDTO | ValueError/KeyError in in-memory adapter (see per-port) | [EVIDENCE:planninghub/application/ports/persistence.py:L31-L45] [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L67-L118] |
| ReservationPersistencePort | planninghub/application/ports/persistence.py | Reservation handlers | CreateReservationRequest, UpdateReservationRequest, GetReservationRequest, ListReservationsRequest | ReservationDTO | ValueError/KeyError in in-memory adapter (see per-port) | [EVIDENCE:planninghub/application/ports/persistence.py:L48-L59] [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L119-L193] |
| ConflictPersistencePort | planninghub/application/ports/persistence.py | Conflict handlers | DetectConflictsRequest, ListConflictsRequest | ConflictDTO | ValueError/KeyError in in-memory adapter (see per-port) | [EVIDENCE:planninghub/application/ports/persistence.py:L62-L67] [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L195-L252] |
| MembershipRepository | planninghub/domain/repositories.py | Domain repository port | Membership | Membership | None defined | [EVIDENCE:planninghub/domain/repositories.py:L11-L25] [EVIDENCE:planninghub/domain/entities.py:L42-L58] |
| ReservationRepository | planninghub/domain/repositories.py | ConflictDetectionService, EvaluateIncomingReservationHandler | Reservation | Reservation | None defined | [EVIDENCE:planninghub/domain/repositories.py:L28-L53] [EVIDENCE:planninghub/domain/services/conflict_detection.py:L23-L52] [EVIDENCE:planninghub/application/handlers/evaluate_incoming_reservation.py:L18-L31] |

## 3. Per-port contract sections

### EvaluateIncomingReservationCommand/Response
- Name: EvaluateIncomingReservationCommand and EvaluateIncomingReservationResponse.
- Responsibility: Carry the reservation evaluation request and return the evaluation response produced by the EvaluateIncomingReservationHandler.
- Input DTO(s):
  - EvaluateIncomingReservationCommand
    - organization_id: str
    - reservation: Reservation
      - id: str
      - organization_id: str
      - resource_id: str | None
      - starts_at_utc: datetime
      - ends_at_utc: datetime
      - timezone: str
      - economic_value: float | None
      - status: ReservationStatus
- Output DTO(s):
  - EvaluateIncomingReservationResponse
    - reservation_id: str
    - conflict: bool
    - proposal: ResolutionProposal | None
      - reservation_id: str
      - strategy_id: str
      - action: str
      - details: dict[str, str]
    - outcome: ResolutionOutcome | None
      - reservation_id: str
      - outcome: ResolutionOutcomeType
      - reason: str
- Error contract (if any): None explicitly defined in handler or port.
- Determinism guarantees: Not specified in the port or handler; deterministic behavior depends on provided repository and strategy implementations.
- MUST NOT: Define adapter behavior or infrastructure details; ports are command/query definitions owned by the application core.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/evaluate_incoming_reservation.py:L12-L23]
  - [EVIDENCE:planninghub/application/handlers/evaluate_incoming_reservation.py:L18-L42]
  - [EVIDENCE:planninghub/domain/entities.py:L106-L122]
  - [EVIDENCE:planninghub/domain/services/conflict_resolution.py:L11-L19]
  - [EVIDENCE:planninghub/domain/services/conflict_outcomes.py:L11-L22]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### CreateUserPort
- Name: CreateUserPort.
- Responsibility: Delegate user creation to the identity persistence port and return CreateUserResponse.
- Input DTO(s):
  - CreateUserRequest
    - email: str
    - display_name: str
- Output DTO(s):
  - CreateUserResponse
    - user: UserDTO
      - id: str
      - email: str
      - display_name: str
      - status: str
- Error contract (if any): None explicitly defined in handler or port.
- Determinism guarantees: Not specified in the port or handler; persistence implementation defines determinism.
- MUST NOT: Include infrastructure details or adapter behavior in the port definition.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/identity.py:L21-L23]
  - [EVIDENCE:planninghub/application/handlers/identity.py:L30-L36]
  - [EVIDENCE:planninghub/application/dtos/identity.py:L9-L40]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### DeactivateUserPort
- Name: DeactivateUserPort.
- Responsibility: Delegate user deactivation to the identity persistence port and return DeactivateUserResponse.
- Input DTO(s):
  - DeactivateUserRequest
    - user_id: str
- Output DTO(s):
  - DeactivateUserResponse
    - user: UserDTO
      - id: str
      - email: str
      - display_name: str
      - status: str
- Error contract (if any): None explicitly defined in handler or port.
- Determinism guarantees: Not specified in the port or handler; persistence implementation defines determinism.
- MUST NOT: Include infrastructure details or adapter behavior in the port definition.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/identity.py:L26-L28]
  - [EVIDENCE:planninghub/application/handlers/identity.py:L39-L45]
  - [EVIDENCE:planninghub/application/dtos/identity.py:L9-L50]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### CreateOrganizationPort
- Name: CreateOrganizationPort.
- Responsibility: Delegate organization creation to the identity persistence port and return CreateOrganizationResponse.
- Input DTO(s):
  - CreateOrganizationRequest
    - name: str
- Output DTO(s):
  - CreateOrganizationResponse
    - organization: OrganizationDTO
      - id: str
      - name: str
- Error contract (if any): None explicitly defined in handler or port.
- Determinism guarantees: Not specified in the port or handler; persistence implementation defines determinism.
- MUST NOT: Include infrastructure details or adapter behavior in the port definition.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/identity.py:L31-L33]
  - [EVIDENCE:planninghub/application/handlers/identity.py:L48-L54]
  - [EVIDENCE:planninghub/application/dtos/identity.py:L17-L60]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### AddMembershipPort
- Name: AddMembershipPort.
- Responsibility: Validate organization_id, prevent duplicate memberships for the same user and organization, then delegate membership creation to the identity persistence port.
- Input DTO(s):
  - AddMembershipRequest
    - user_id: str
    - organization_id: str
    - role: str
- Output DTO(s):
  - AddMembershipResponse
    - membership: MembershipDTO
      - id: str
      - user_id: str
      - organization_id: str
      - role: str
- Error contract (if any):
  - ValueError when organization_id is empty.
  - ValueError when a duplicate membership is detected for user_id and organization_id.
- Determinism guarantees: Not specified in the port or handler; persistence implementation defines determinism.
- MUST NOT: Include infrastructure details or adapter behavior in the port definition.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/identity.py:L36-L38]
  - [EVIDENCE:planninghub/application/handlers/identity.py:L20-L72]
  - [EVIDENCE:planninghub/application/dtos/identity.py:L23-L72]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### ListMembershipsPort
- Name: ListMembershipsPort.
- Responsibility: Validate optional filter IDs and delegate membership listing to the identity persistence port.
- Input DTO(s):
  - ListMembershipsRequest
    - user_id: str | None
    - organization_id: str | None
- Output DTO(s):
  - ListMembershipsResponse
    - memberships: list[MembershipDTO]
      - id: str
      - user_id: str
      - organization_id: str
      - role: str
- Error contract (if any):
  - ValueError when user_id is provided as an empty string.
  - ValueError when organization_id is provided as an empty string.
- Determinism guarantees: Not specified in the port or handler; persistence implementation defines determinism.
- MUST NOT: Include infrastructure details or adapter behavior in the port definition.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/identity.py:L41-L43]
  - [EVIDENCE:planninghub/application/handlers/identity.py:L25-L83]
  - [EVIDENCE:planninghub/application/dtos/identity.py:L23-L82]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### CreateReservationPort
- Name: CreateReservationPort.
- Responsibility: Validate organization_id and reservation interval, then delegate reservation creation to the reservation persistence port.
- Input DTO(s):
  - CreateReservationRequest
    - organization_id: str
    - resource_id: str | None
    - starts_at_utc: datetime
    - ends_at_utc: datetime
    - timezone: str
    - economic_value: float | None
- Output DTO(s):
  - CreateReservationResponse
    - reservation: ReservationDTO
      - id: str
      - organization_id: str
      - resource_id: str | None
      - starts_at_utc: datetime
      - ends_at_utc: datetime
      - timezone: str
      - economic_value: float | None
      - status: str
- Error contract (if any):
  - ValueError when organization_id is empty.
  - ValueError when starts_at_utc >= ends_at_utc.
- Determinism guarantees: Not specified in the port or handler; persistence implementation defines determinism.
- MUST NOT: Include infrastructure details or adapter behavior in the port definition.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/time_reservation.py:L19-L21]
  - [EVIDENCE:planninghub/application/handlers/time_reservation.py:L18-L36]
  - [EVIDENCE:planninghub/application/dtos/time_reservation.py:L10-L40]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### UpdateReservationPort
- Name: UpdateReservationPort.
- Responsibility: Validate the interval when both timestamps are provided and delegate updates to the reservation persistence port.
- Input DTO(s):
  - UpdateReservationRequest
    - reservation_id: str
    - starts_at_utc: datetime | None
    - ends_at_utc: datetime | None
    - resource_id: str | None
    - status: str | None
- Output DTO(s):
  - UpdateReservationResponse
    - reservation: ReservationDTO
      - id: str
      - organization_id: str
      - resource_id: str | None
      - starts_at_utc: datetime
      - ends_at_utc: datetime
      - timezone: str
      - economic_value: float | None
      - status: str
- Error contract (if any):
  - ValueError when both starts_at_utc and ends_at_utc are provided and starts_at_utc >= ends_at_utc.
- Determinism guarantees: Not specified in the port or handler; persistence implementation defines determinism.
- MUST NOT: Include infrastructure details or adapter behavior in the port definition.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/time_reservation.py:L24-L26]
  - [EVIDENCE:planninghub/application/handlers/time_reservation.py:L39-L47]
  - [EVIDENCE:planninghub/application/dtos/time_reservation.py:L10-L55]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### GetReservationPort
- Name: GetReservationPort.
- Responsibility: Delegate reservation retrieval to the reservation persistence port and wrap the result.
- Input DTO(s):
  - GetReservationRequest
    - reservation_id: str
- Output DTO(s):
  - GetReservationResponse
    - reservation: ReservationDTO
      - id: str
      - organization_id: str
      - resource_id: str | None
      - starts_at_utc: datetime
      - ends_at_utc: datetime
      - timezone: str
      - economic_value: float | None
      - status: str
- Error contract (if any): None explicitly defined in handler or port.
- Determinism guarantees: Not specified in the port or handler; persistence implementation defines determinism.
- MUST NOT: Include infrastructure details or adapter behavior in the port definition.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/time_reservation.py:L29-L31]
  - [EVIDENCE:planninghub/application/handlers/time_reservation.py:L50-L56]
  - [EVIDENCE:planninghub/application/dtos/time_reservation.py:L10-L65]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### ListReservationsPort
- Name: ListReservationsPort.
- Responsibility: Validate organization_id and delegate reservation listing to the reservation persistence port.
- Input DTO(s):
  - ListReservationsRequest
    - organization_id: str
    - resource_id: str | None
    - time_range: TimeRangeDTO | None
      - start_utc: datetime
      - end_utc: datetime
- Output DTO(s):
  - ListReservationsResponse
    - reservations: list[ReservationDTO]
      - id: str
      - organization_id: str
      - resource_id: str | None
      - starts_at_utc: datetime
      - ends_at_utc: datetime
      - timezone: str
      - economic_value: float | None
      - status: str
- Error contract (if any):
  - ValueError when organization_id is empty.
- Determinism guarantees: Not specified in the port or handler; persistence implementation defines determinism.
- MUST NOT: Include infrastructure details or adapter behavior in the port definition.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/time_reservation.py:L34-L36]
  - [EVIDENCE:planninghub/application/handlers/time_reservation.py:L59-L66]
  - [EVIDENCE:planninghub/application/dtos/time_reservation.py:L10-L76]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### DetectConflictsPort
- Name: DetectConflictsPort.
- Responsibility: Validate organization_id and delegate conflict detection to the conflict persistence port.
- Input DTO(s):
  - DetectConflictsRequest
    - organization_id: str
    - reservation_id: str
- Output DTO(s):
  - DetectConflictsResponse
    - conflicts: list[ConflictDTO]
      - id: str
      - organization_id: str
      - reservation_id: str
      - resource_id: str | None
      - severity: str
      - reason: str
- Error contract (if any):
  - ValueError when organization_id is empty.
- Determinism guarantees: Not specified in the port or handler; persistence implementation defines determinism.
- MUST NOT: Include infrastructure details or adapter behavior in the port definition.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/conflict.py:L15-L17]
  - [EVIDENCE:planninghub/application/handlers/conflict.py:L14-L31]
  - [EVIDENCE:planninghub/application/dtos/conflict.py:L9-L28]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### ListConflictsPort
- Name: ListConflictsPort.
- Responsibility: Validate organization_id and reservation_id filters, then delegate conflict listing to the conflict persistence port.
- Input DTO(s):
  - ListConflictsRequest
    - organization_id: str
    - reservation_id: str | None
- Output DTO(s):
  - ListConflictsResponse
    - conflicts: list[ConflictDTO]
      - id: str
      - organization_id: str
      - reservation_id: str
      - resource_id: str | None
      - severity: str
      - reason: str
- Error contract (if any):
  - ValueError when organization_id is empty.
  - ValueError when reservation_id is provided as an empty string.
- Determinism guarantees: Not specified in the port or handler; persistence implementation defines determinism.
- MUST NOT: Include infrastructure details or adapter behavior in the port definition.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/conflict.py:L20-L22]
  - [EVIDENCE:planninghub/application/handlers/conflict.py:L14-L42]
  - [EVIDENCE:planninghub/application/dtos/conflict.py:L9-L38]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L16-L31]

### IdentityPersistencePort
- Name: IdentityPersistencePort.
- Responsibility: Persist identity DTOs for users, organizations, and memberships.
- Input DTO(s):
  - CreateUserRequest (email: str, display_name: str)
  - DeactivateUserRequest (user_id: str)
  - CreateOrganizationRequest (name: str)
  - AddMembershipRequest (user_id: str, organization_id: str, role: str)
  - ListMembershipsRequest (user_id: str | None, organization_id: str | None)
- Output DTO(s):
  - UserDTO (id: str, email: str, display_name: str, status: str)
  - OrganizationDTO (id: str, name: str)
  - MembershipDTO (id: str, user_id: str, organization_id: str, role: str)
- Error contract (if any):
  - InMemoryPersistenceAdapter raises ValueError for empty organization_id, invalid roles, or duplicate memberships.
  - InMemoryPersistenceAdapter raises KeyError when deactivating a missing user.
- Determinism guarantees: InMemoryPersistenceAdapter uses incrementing counters for deterministic IDs.
- MUST NOT: Add business logic beyond invariants already enforced by the domain and adapters.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/persistence.py:L31-L45]
  - [EVIDENCE:planninghub/application/dtos/identity.py:L9-L82]
  - [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L49-L118]
  - [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L254-L272]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L6-L31]

### ReservationPersistencePort
- Name: ReservationPersistencePort.
- Responsibility: Persist reservation DTOs and provide reservation lookups.
- Input DTO(s):
  - CreateReservationRequest (organization_id: str, resource_id: str | None, starts_at_utc: datetime, ends_at_utc: datetime, timezone: str, economic_value: float | None)
  - UpdateReservationRequest (reservation_id: str, starts_at_utc: datetime | None, ends_at_utc: datetime | None, resource_id: str | None, status: str | None)
  - GetReservationRequest (reservation_id: str)
  - ListReservationsRequest (organization_id: str, resource_id: str | None, time_range: TimeRangeDTO | None)
- Output DTO(s):
  - ReservationDTO (id: str, organization_id: str, resource_id: str | None, starts_at_utc: datetime, ends_at_utc: datetime, timezone: str, economic_value: float | None, status: str)
- Error contract (if any):
  - InMemoryPersistenceAdapter raises ValueError for empty organization_id, invalid intervals, or invalid reservation status values.
  - InMemoryPersistenceAdapter raises KeyError when updating or fetching missing reservations.
- Determinism guarantees: InMemoryPersistenceAdapter uses incrementing counters for deterministic IDs.
- MUST NOT: Add business logic beyond invariants already enforced by the domain and adapters.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/persistence.py:L48-L59]
  - [EVIDENCE:planninghub/application/dtos/time_reservation.py:L10-L76]
  - [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L119-L193]
  - [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L254-L287]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L6-L31]

### ConflictPersistencePort
- Name: ConflictPersistencePort.
- Responsibility: Persist and list conflict DTOs for reservations.
- Input DTO(s):
  - DetectConflictsRequest (organization_id: str, reservation_id: str)
  - ListConflictsRequest (organization_id: str, reservation_id: str | None)
- Output DTO(s):
  - ConflictDTO (id: str, organization_id: str, reservation_id: str, resource_id: str | None, severity: str, reason: str)
- Error contract (if any):
  - InMemoryPersistenceAdapter raises ValueError for empty organization_id or reservation org mismatch.
  - InMemoryPersistenceAdapter raises KeyError when referencing missing reservations.
- Determinism guarantees: InMemoryPersistenceAdapter uses incrementing counters for deterministic IDs.
- MUST NOT: Add business logic beyond invariants already enforced by the domain and adapters.
- Evidence:
  - [EVIDENCE:planninghub/application/ports/persistence.py:L62-L67]
  - [EVIDENCE:planninghub/application/dtos/conflict.py:L9-L38]
  - [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L195-L252]
  - [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L254-L287]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L6-L31]

### MembershipRepository
- Name: MembershipRepository.
- Responsibility: Persist and fetch Membership domain entities.
- Input DTO(s):
  - Membership
    - id: str
    - organization_id: str
    - user_id: str
    - role: MembershipRole
- Output DTO(s):
  - Membership | None
- Error contract (if any): None defined in the repository protocol.
- Determinism guarantees: Not specified in the port.
- MUST NOT: Depend on application or infrastructure layers.
- Evidence:
  - [EVIDENCE:planninghub/domain/repositories.py:L11-L25]
  - [EVIDENCE:planninghub/domain/entities.py:L42-L58]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L11-L15]

### ReservationRepository
- Name: ReservationRepository.
- Responsibility: Persist and query Reservation domain entities, including overlap queries.
- Input DTO(s):
  - Reservation
    - id: str
    - organization_id: str
    - resource_id: str | None
    - starts_at_utc: datetime
    - ends_at_utc: datetime
    - timezone: str
    - economic_value: float | None
    - status: ReservationStatus
- Output DTO(s):
  - Reservation | None
- Error contract (if any): None defined in the repository protocol.
- Determinism guarantees: Not specified in the port.
- MUST NOT: Depend on application or infrastructure layers.
- Evidence:
  - [EVIDENCE:planninghub/domain/repositories.py:L28-L53]
  - [EVIDENCE:planninghub/domain/entities.py:L106-L122]
  - [EVIDENCE:docs/specs/architecture/hexagonal_architecture_contract.md:L11-L15]

## 4. Adapter contracts (http, persistence, in-memory)

### HTTP adapter (reservation evaluation)
- Responsibilities:
  - Accept a request dict, bind it to EvaluateIncomingReservationRequestDTO, map to EvaluateIncomingReservationCommand, run the handler, and map the response DTO back to a dict.
  - Convert TypeError or ValueError during request mapping to HTTP 400 with "invalid request payload".
- Mapping rules:
  - request_dto_to_command parses starts_at_utc_iso and ends_at_utc_iso using datetime.fromisoformat and builds a Reservation with economic_value=None and status=ReservationStatus.ACTIVE.
  - response_to_response_dto maps reservation_id, conflict, outcome, action, and details fields from the application response.
- Ordering/ID rules: None defined.
- Evidence:
  - [EVIDENCE:planninghub/adapters/http/dtos.py:L8-L24]
  - [EVIDENCE:planninghub/adapters/http/mappers.py:L19-L49]
  - [EVIDENCE:planninghub/adapters/fastapi_app/routes.py:L16-L39]

### Persistence adapters
- Responsibilities:
  - StubPersistenceAdapter defines the persistence port surface and raises NotImplementedError for all methods.
  - InMemoryPersistenceAdapter implements persistence ports in memory with deterministic ID counters, validation, and conflict detection.
- Mapping rules:
  - DTO field values are mapped directly into stored DTOs with explicit status, severity, and reason strings where set.
- Ordering/ID rules:
  - InMemoryPersistenceAdapter generates IDs using incrementing counters per prefix via _next_id.
  - Conflict detection assigns severity "high" and reason "overlap:<other-id>" for overlaps.
- Evidence:
  - [EVIDENCE:planninghub/adapters/persistence/stub.py:L34-L70]
  - [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L49-L287]

### In-memory domain repositories
- Responsibilities:
  - InMemoryMembershipRepository stores Membership entities and returns sorted lists by membership.id.
  - InMemoryReservationRepository stores Reservation entities and returns sorted lists by id or by (starts_at_utc, id) for overlaps.
- Mapping rules:
  - Domain entities are stored as-is without transformation.
- Ordering/ID rules:
  - list_by_org and list_by_resource sort by id.
  - list_overlapping sorts by starts_at_utc then id.
- Evidence:
  - [EVIDENCE:planninghub/infra/repositories_in_memory.py:L11-L92]

## 5. Locked contracts
The following contracts are frozen and changes require an explicit DECISION note in docs/decisions and a spec update:
- Application port definitions and DTOs under planninghub/application/ports and planninghub/application/dtos.
- Reservation evaluation command/response and handler wiring in planninghub/application/ports/evaluate_incoming_reservation.py and planninghub/application/handlers/evaluate_incoming_reservation.py.
- Persistence port definitions under planninghub/application/ports/persistence.py and adapter DTOs under planninghub/adapters/http.
- Domain repository ports under planninghub/domain/repositories.py and in-memory implementations under planninghub/infra/repositories_in_memory.py.
- InMemoryPersistenceAdapter behavior in planninghub/adapters/persistence/in_memory.py.

Evidence:
- [EVIDENCE:planninghub/application/ports/evaluate_incoming_reservation.py:L12-L23]
- [EVIDENCE:planninghub/application/ports/identity.py:L21-L43]
- [EVIDENCE:planninghub/application/ports/time_reservation.py:L19-L36]
- [EVIDENCE:planninghub/application/ports/conflict.py:L15-L22]
- [EVIDENCE:planninghub/application/ports/persistence.py:L31-L67]
- [EVIDENCE:planninghub/application/dtos/identity.py:L9-L82]
- [EVIDENCE:planninghub/application/dtos/time_reservation.py:L10-L76]
- [EVIDENCE:planninghub/application/dtos/conflict.py:L9-L38]
- [EVIDENCE:planninghub/application/handlers/evaluate_incoming_reservation.py:L18-L42]
- [EVIDENCE:planninghub/adapters/http/dtos.py:L8-L24]
- [EVIDENCE:planninghub/adapters/http/mappers.py:L19-L49]
- [EVIDENCE:planninghub/domain/repositories.py:L11-L53]
- [EVIDENCE:planninghub/infra/repositories_in_memory.py:L11-L92]
- [EVIDENCE:planninghub/adapters/persistence/in_memory.py:L49-L287]
