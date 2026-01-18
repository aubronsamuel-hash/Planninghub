# Real Persistence Adapter Contract

## Purpose and scope
- Provide a contract for a real (non in-memory) persistence adapter that implements the
  existing persistence ports for identity, reservations, and conflicts.
- Define behavioral guarantees that the application core can rely on without selecting
  any storage technology or schema.
- Explicitly does not select databases, schemas, migrations, replication, caching, or
  transport protocols.
- Explicitly does not introduce new domain rules, validation beyond existing specs, or
  scheduling logic.

## Covered ports
- IdentityPersistencePort
- ReservationPersistencePort
- ConflictPersistencePort

## Transaction boundaries
- Each write operation (create, update, deactivate, add) MUST be atomic for the entity
  or membership it modifies.
- A write MUST either fully apply or have no effect.
- Read operations (get, list, detect) MUST operate on a coherent snapshot of persisted
  data within the adapter.
- List and detect operations MAY be eventually consistent with concurrent writes, but
  MUST NOT return partial or internally inconsistent records.

### Write operations (atomic per method call)
- IdentityPersistencePort: CreateUser, DeactivateUser, CreateOrganization,
  AddMembership.
- ReservationPersistencePort: CreateReservation, UpdateReservation.
- ConflictPersistencePort: no write operations are defined in the current ports.
- Atomicity is scoped to each individual method call and MUST NOT span multiple calls.

## ID strategy (contractual)
- IDs MUST be stable once created and MUST NOT change on updates.
- IDs MUST be unique within their entity namespace across all organizations.
- IDs MUST be treated as opaque by the application; no semantic meaning is required.
- The adapter MUST return the assigned IDs in responses.
- Implementation details (generation, storage, encoding) are intentionally unspecified.

## Ordering guarantees
- List operations MUST return a deterministic order for the same request and data
  snapshot.
- If the request includes explicit ordering semantics in the port contract, the adapter
  MUST honor them.
- If no ordering semantics are specified, the order is undefined beyond determinism.

## Concurrency expectations
- The adapter MUST tolerate concurrent requests across all covered ports without data
  corruption or broken invariants.
- The adapter MUST NOT allow silent lost updates.
- Concurrent writes to the same entity MUST either yield a deterministic last-write
  outcome with a well-defined final state or be rejected with a domain error.
- The adapter is not required to provide global serializability or distributed locking
  across unrelated entities.

## Error contract
- Domain error: invalid inputs or invariant violations MUST surface as a domain error.
- Not found error: requests for missing entities MUST surface as a not found error.
- Infrastructure error: storage unavailability, timeouts, or IO failures MUST surface
  as an infrastructure error.
- The adapter MUST distinguish these error categories.
- Vendor-specific error details or internal storage metadata MUST NOT leak to the
  application.

## Determinism
- Given identical inputs and identical persisted state, read operations MUST return the
  same results.
- Write operations MUST return the persisted record as stored after the write.
- ID formats, latency, and internal batching MAY vary by implementation.

## MUST NOT
- MUST NOT introduce new business rules or modify existing domain invariants.
- MUST NOT silently drop or coerce invalid inputs without a domain error.
- MUST NOT expose or depend on storage-specific features in the port contract.
- MUST NOT return records from outside the requested organization scope.
