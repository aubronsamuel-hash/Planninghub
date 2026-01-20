"""SQLite persistence adapter."""

from __future__ import annotations

import sqlite3
from dataclasses import replace
from datetime import datetime

from planninghub.application.dtos.conflict import (
    ConflictDTO,
    DetectConflictsRequest,
    ListConflictsRequest,
)
from planninghub.application.dtos.identity import (
    AddMembershipRequest,
    CreateOrganizationRequest,
    CreateUserRequest,
    DeactivateUserRequest,
    ListMembershipsRequest,
    MembershipDTO,
    OrganizationDTO,
    UserDTO,
)
from planninghub.application.dtos.time_reservation import (
    CreateReservationRequest,
    GetReservationRequest,
    ListReservationsRequest,
    ReservationDTO,
    TimeRangeDTO,
    UpdateReservationRequest,
)
from planninghub.application.ports.persistence import (
    ConflictPersistencePort,
    IdentityPersistencePort,
    ReservationPersistencePort,
)

ROLE_VALUES = {"owner", "admin", "member"}
RESERVATION_STATUS_VALUES = {"draft", "active", "cancelled"}
CONFLICT_SEVERITY_VALUES = {"critical", "high", "medium", "low"}


class SQLitePersistenceAdapter(
    IdentityPersistencePort,
    ReservationPersistencePort,
    ConflictPersistencePort,
):
    """SQLite-backed persistence adapter."""

    def __init__(
        self,
        db_path: str | None = None,
        connection: sqlite3.Connection | None = None,
    ) -> None:
        if connection is not None and db_path is not None:
            raise ValueError("Provide either db_path or connection, not both.")
        if connection is None:
            connection = sqlite3.connect(db_path or ":memory:")
        connection.row_factory = sqlite3.Row
        self._connection = connection
        with self._connection:
            self._ensure_schema()

    def create_user(self, request: CreateUserRequest) -> UserDTO:
        with self._connection:
            user_id = self._next_id("user")
            user = UserDTO(
                id=user_id,
                email=request.email,
                display_name=request.display_name,
                status="active",
            )
            self._connection.execute(
                "INSERT INTO users (id, email, display_name, status) VALUES (?, ?, ?, ?)",
                (user.id, user.email, user.display_name, user.status),
            )
        return user

    def deactivate_user(self, request: DeactivateUserRequest) -> UserDTO:
        with self._connection:
            user = self._get_required_user(request.user_id)
            updated = replace(user, status="inactive")
            self._connection.execute(
                "UPDATE users SET status = ? WHERE id = ?",
                (updated.status, updated.id),
            )
        return updated

    def create_organization(self, request: CreateOrganizationRequest) -> OrganizationDTO:
        with self._connection:
            organization_id = self._next_id("org")
            organization = OrganizationDTO(id=organization_id, name=request.name)
            self._connection.execute(
                "INSERT INTO organizations (id, name) VALUES (?, ?)",
                (organization.id, organization.name),
            )
        return organization

    def add_membership(self, request: AddMembershipRequest) -> MembershipDTO:
        self._require_organization_id(request.organization_id, "membership")
        self._require_role(request.role)
        with self._connection:
            existing = self._connection.execute(
                "SELECT id FROM memberships WHERE user_id = ? AND organization_id = ?",
                (request.user_id, request.organization_id),
            ).fetchone()
            if existing is not None:
                raise ValueError("Duplicate membership for user and organization.")
            membership_id = self._next_id("mem")
            membership = MembershipDTO(
                id=membership_id,
                user_id=request.user_id,
                organization_id=request.organization_id,
                role=request.role,
            )
            try:
                self._connection.execute(
                    """
                    INSERT INTO memberships (id, user_id, organization_id, role)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        membership.id,
                        membership.user_id,
                        membership.organization_id,
                        membership.role,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise ValueError("Duplicate membership for user and organization.") from exc
        return membership

    def list_memberships(self, request: ListMembershipsRequest) -> list[MembershipDTO]:
        if request.organization_id is not None:
            self._require_organization_id(request.organization_id, "membership")
        query = "SELECT id, user_id, organization_id, role FROM memberships"
        clauses: list[str] = []
        params: list[str] = []
        if request.user_id is not None:
            clauses.append("user_id = ?")
            params.append(request.user_id)
        if request.organization_id is not None:
            clauses.append("organization_id = ?")
            params.append(request.organization_id)
        if clauses:
            query = f"{query} WHERE {' AND '.join(clauses)}"
        query = f"{query} ORDER BY rowid"
        rows = self._connection.execute(query, params).fetchall()
        return [self._row_to_membership(row) for row in rows]

    def create_reservation(self, request: CreateReservationRequest) -> ReservationDTO:
        self._require_organization_id(request.organization_id, "reservation")
        self._require_valid_interval(request.starts_at_utc, request.ends_at_utc)
        with self._connection:
            reservation_id = self._next_id("res")
            reservation = ReservationDTO(
                id=reservation_id,
                organization_id=request.organization_id,
                resource_id=request.resource_id,
                starts_at_utc=request.starts_at_utc,
                ends_at_utc=request.ends_at_utc,
                timezone=request.timezone,
                economic_value=request.economic_value,
                status="draft",
            )
            self._connection.execute(
                """
                INSERT INTO reservations (
                    id,
                    organization_id,
                    resource_id,
                    starts_at_utc,
                    ends_at_utc,
                    timezone,
                    economic_value,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    reservation.id,
                    reservation.organization_id,
                    reservation.resource_id,
                    reservation.starts_at_utc.isoformat(),
                    reservation.ends_at_utc.isoformat(),
                    reservation.timezone,
                    reservation.economic_value,
                    reservation.status,
                ),
            )
        return reservation

    def update_reservation(self, request: UpdateReservationRequest) -> ReservationDTO:
        with self._connection:
            reservation = self._get_required_reservation(request.reservation_id)
            starts_at_utc = request.starts_at_utc or reservation.starts_at_utc
            ends_at_utc = request.ends_at_utc or reservation.ends_at_utc
            self._require_valid_interval(starts_at_utc, ends_at_utc)
            resource_id = (
                reservation.resource_id
                if request.resource_id is None
                else request.resource_id
            )
            status = reservation.status
            if request.status is not None:
                self._require_reservation_status(request.status)
                status = request.status
            updated = ReservationDTO(
                id=reservation.id,
                organization_id=reservation.organization_id,
                resource_id=resource_id,
                starts_at_utc=starts_at_utc,
                ends_at_utc=ends_at_utc,
                timezone=reservation.timezone,
                economic_value=reservation.economic_value,
                status=status,
            )
            self._connection.execute(
                """
                UPDATE reservations
                SET resource_id = ?,
                    starts_at_utc = ?,
                    ends_at_utc = ?,
                    status = ?
                WHERE id = ?
                """,
                (
                    updated.resource_id,
                    updated.starts_at_utc.isoformat(),
                    updated.ends_at_utc.isoformat(),
                    updated.status,
                    updated.id,
                ),
            )
        return updated

    def get_reservation(self, request: GetReservationRequest) -> ReservationDTO:
        return self._get_required_reservation(request.reservation_id)

    def list_reservations(self, request: ListReservationsRequest) -> list[ReservationDTO]:
        self._require_organization_id(request.organization_id, "reservation")
        query = (
            "SELECT id, organization_id, resource_id, starts_at_utc, ends_at_utc, "
            "timezone, economic_value, status "
            "FROM reservations WHERE organization_id = ?"
        )
        params: list[str | None] = [request.organization_id]
        if request.resource_id is not None:
            query = f"{query} AND resource_id = ?"
            params.append(request.resource_id)
        query = f"{query} ORDER BY rowid"
        rows = self._connection.execute(query, params).fetchall()
        reservations = [self._row_to_reservation(row) for row in rows]
        if request.time_range is not None:
            self._require_valid_interval(
                request.time_range.start_utc,
                request.time_range.end_utc,
            )
            reservations = [
                reservation
                for reservation in reservations
                if self._overlaps(
                    reservation.starts_at_utc,
                    reservation.ends_at_utc,
                    request.time_range,
                )
            ]
        return reservations

    def detect_conflicts(self, request: DetectConflictsRequest) -> list[ConflictDTO]:
        self._require_organization_id(request.organization_id, "conflict")
        with self._connection:
            reservation = self._get_required_reservation(request.reservation_id)
            if reservation.organization_id != request.organization_id:
                raise ValueError("Reservation is not scoped to the organization.")
            conflicts: list[ConflictDTO] = []
            if reservation.resource_id is not None:
                rows = self._connection.execute(
                    """
                    SELECT id, organization_id, resource_id, starts_at_utc, ends_at_utc,
                           timezone, economic_value, status
                    FROM reservations
                    WHERE organization_id = ? AND resource_id = ? AND id != ?
                    ORDER BY rowid
                    """,
                    (
                        reservation.organization_id,
                        reservation.resource_id,
                        reservation.id,
                    ),
                ).fetchall()
                for row in rows:
                    other = self._row_to_reservation(row)
                    if not self._overlaps(
                        reservation.starts_at_utc,
                        reservation.ends_at_utc,
                        TimeRangeDTO(
                            start_utc=other.starts_at_utc,
                            end_utc=other.ends_at_utc,
                        ),
                    ):
                        continue
                    conflict = self._get_conflict_for_pair(reservation.id, other.id)
                    if conflict is None:
                        self._require_conflict_severity("high")
                        conflict_id = self._next_id("conf")
                        conflict = ConflictDTO(
                            id=conflict_id,
                            organization_id=reservation.organization_id,
                            reservation_id=reservation.id,
                            resource_id=reservation.resource_id,
                            severity="high",
                            reason=f"overlap:{other.id}",
                        )
                        try:
                            self._connection.execute(
                                """
                                INSERT INTO conflicts (
                                    id,
                                    organization_id,
                                    reservation_id,
                                    resource_id,
                                    severity,
                                    reason,
                                    other_reservation_id
                                )
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                """,
                                (
                                    conflict.id,
                                    conflict.organization_id,
                                    conflict.reservation_id,
                                    conflict.resource_id,
                                    conflict.severity,
                                    conflict.reason,
                                    other.id,
                                ),
                            )
                        except sqlite3.IntegrityError:
                            conflict = self._get_conflict_for_pair(
                                reservation.id,
                                other.id,
                            )
                            if conflict is None:
                                raise
                    conflicts.append(conflict)
        return conflicts

    def list_conflicts(self, request: ListConflictsRequest) -> list[ConflictDTO]:
        self._require_organization_id(request.organization_id, "conflict")
        query = (
            "SELECT id, organization_id, reservation_id, resource_id, severity, reason "
            "FROM conflicts WHERE organization_id = ?"
        )
        params: list[str] = [request.organization_id]
        if request.reservation_id is not None:
            query = f"{query} AND reservation_id = ?"
            params.append(request.reservation_id)
        query = f"{query} ORDER BY rowid"
        rows = self._connection.execute(query, params).fetchall()
        return [self._row_to_conflict(row) for row in rows]

    def _ensure_schema(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                display_name TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS organizations (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memberships (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                organization_id TEXT NOT NULL,
                role TEXT NOT NULL,
                UNIQUE(user_id, organization_id)
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reservations (
                id TEXT PRIMARY KEY,
                organization_id TEXT NOT NULL,
                resource_id TEXT,
                starts_at_utc TEXT NOT NULL,
                ends_at_utc TEXT NOT NULL,
                timezone TEXT NOT NULL,
                economic_value REAL,
                status TEXT NOT NULL
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS conflicts (
                id TEXT PRIMARY KEY,
                organization_id TEXT NOT NULL,
                reservation_id TEXT NOT NULL,
                resource_id TEXT,
                severity TEXT NOT NULL,
                reason TEXT NOT NULL,
                other_reservation_id TEXT NOT NULL,
                UNIQUE(reservation_id, other_reservation_id)
            )
            """
        )
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS counters (
                prefix TEXT PRIMARY KEY,
                value INTEGER NOT NULL
            )
            """
        )
        self._ensure_counters()

    def _ensure_counters(self) -> None:
        self._connection.executemany(
            "INSERT OR IGNORE INTO counters (prefix, value) VALUES (?, ?)",
            [(prefix, 0) for prefix in ("user", "org", "mem", "res", "conf")],
        )

    def _next_id(self, prefix: str) -> str:
        row = self._connection.execute(
            "SELECT value FROM counters WHERE prefix = ?",
            (prefix,),
        ).fetchone()
        if row is None:
            raise KeyError(f"counter not found: {prefix}")
        value = row["value"] + 1
        self._connection.execute(
            "UPDATE counters SET value = ? WHERE prefix = ?",
            (value, prefix),
        )
        return f"{prefix}-{value}"

    def _get_required_user(self, user_id: str) -> UserDTO:
        row = self._connection.execute(
            "SELECT id, email, display_name, status FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        if row is None:
            raise KeyError(f"user not found: {user_id}")
        return self._row_to_user(row)

    def _get_required_reservation(self, reservation_id: str) -> ReservationDTO:
        row = self._connection.execute(
            """
            SELECT id, organization_id, resource_id, starts_at_utc, ends_at_utc,
                   timezone, economic_value, status
            FROM reservations
            WHERE id = ?
            """,
            (reservation_id,),
        ).fetchone()
        if row is None:
            raise KeyError(f"reservation not found: {reservation_id}")
        return self._row_to_reservation(row)

    def _get_conflict_for_pair(
        self,
        reservation_id: str,
        other_reservation_id: str,
    ) -> ConflictDTO | None:
        row = self._connection.execute(
            """
            SELECT id, organization_id, reservation_id, resource_id, severity, reason
            FROM conflicts
            WHERE reservation_id = ? AND other_reservation_id = ?
            """,
            (reservation_id, other_reservation_id),
        ).fetchone()
        if row is None:
            return None
        return self._row_to_conflict(row)

    @staticmethod
    def _row_to_user(row: sqlite3.Row) -> UserDTO:
        return UserDTO(
            id=row["id"],
            email=row["email"],
            display_name=row["display_name"],
            status=row["status"],
        )

    @staticmethod
    def _row_to_membership(row: sqlite3.Row) -> MembershipDTO:
        return MembershipDTO(
            id=row["id"],
            user_id=row["user_id"],
            organization_id=row["organization_id"],
            role=row["role"],
        )

    @staticmethod
    def _row_to_reservation(row: sqlite3.Row) -> ReservationDTO:
        return ReservationDTO(
            id=row["id"],
            organization_id=row["organization_id"],
            resource_id=row["resource_id"],
            starts_at_utc=datetime.fromisoformat(row["starts_at_utc"]),
            ends_at_utc=datetime.fromisoformat(row["ends_at_utc"]),
            timezone=row["timezone"],
            economic_value=row["economic_value"],
            status=row["status"],
        )

    @staticmethod
    def _row_to_conflict(row: sqlite3.Row) -> ConflictDTO:
        return ConflictDTO(
            id=row["id"],
            organization_id=row["organization_id"],
            reservation_id=row["reservation_id"],
            resource_id=row["resource_id"],
            severity=row["severity"],
            reason=row["reason"],
        )

    @staticmethod
    def _require_organization_id(organization_id: str, label: str) -> None:
        if not organization_id:
            raise ValueError(f"{label} requires a non-empty organization_id.")

    @staticmethod
    def _require_role(role: str) -> None:
        if role not in ROLE_VALUES:
            raise ValueError("Role must be one of: owner, admin, member.")

    @staticmethod
    def _require_reservation_status(status: str) -> None:
        if status not in RESERVATION_STATUS_VALUES:
            raise ValueError("Status must be one of: draft, active, cancelled.")

    @staticmethod
    def _require_conflict_severity(severity: str) -> None:
        if severity not in CONFLICT_SEVERITY_VALUES:
            raise ValueError("Severity must be one of: critical, high, medium, low.")

    @staticmethod
    def _require_valid_interval(starts_at_utc: datetime, ends_at_utc: datetime) -> None:
        if starts_at_utc >= ends_at_utc:
            raise ValueError("Reservation interval must have starts_at_utc < ends_at_utc.")

    @staticmethod
    def _overlaps(starts_at_utc: datetime, ends_at_utc: datetime, time_range: TimeRangeDTO) -> bool:
        return starts_at_utc < time_range.end_utc and ends_at_utc > time_range.start_utc
