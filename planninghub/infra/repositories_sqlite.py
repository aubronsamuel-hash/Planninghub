"""SQLite-backed repository implementations."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from planninghub.domain.entities import Membership, Reservation
from planninghub.domain.value_objects import MembershipRole, ReservationStatus


class SQLiteMembershipRepository:
    """SQLite membership repository."""

    def __init__(
        self,
        db_path: str | None = None,
        connection: sqlite3.Connection | None = None,
    ) -> None:
        if db_path is not None and connection is not None:
            raise ValueError("Provide either db_path or connection, not both.")
        if connection is None:
            connection = sqlite3.connect(db_path or ":memory:", check_same_thread=False)
        connection.row_factory = sqlite3.Row
        self._connection = connection
        with self._connection:
            self._ensure_schema()

    def add(self, membership: Membership) -> None:
        with self._connection:
            self._connection.execute(
                """
                INSERT OR REPLACE INTO memberships (id, organization_id, user_id, role)
                VALUES (?, ?, ?, ?)
                """,
                (
                    membership.id,
                    membership.organization_id,
                    membership.user_id,
                    membership.role.value,
                ),
            )

    def get_by_id(self, membership_id: str) -> Membership | None:
        row = self._connection.execute(
            """
            SELECT id, organization_id, user_id, role
            FROM memberships
            WHERE id = ?
            """,
            (membership_id,),
        ).fetchone()
        if row is None:
            return None
        return self._row_to_membership(row)

    def list_by_org(self, organization_id: str) -> list[Membership]:
        rows = self._connection.execute(
            """
            SELECT id, organization_id, user_id, role
            FROM memberships
            WHERE organization_id = ?
            ORDER BY id
            """,
            (organization_id,),
        ).fetchall()
        return [self._row_to_membership(row) for row in rows]

    def find_by_user(self, organization_id: str, user_id: str) -> list[Membership]:
        rows = self._connection.execute(
            """
            SELECT id, organization_id, user_id, role
            FROM memberships
            WHERE organization_id = ? AND user_id = ?
            ORDER BY id
            """,
            (organization_id, user_id),
        ).fetchall()
        return [self._row_to_membership(row) for row in rows]

    def _ensure_schema(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memberships (
                id TEXT PRIMARY KEY,
                organization_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL
            )
            """
        )

    @staticmethod
    def _row_to_membership(row: sqlite3.Row) -> Membership:
        return Membership(
            id=row["id"],
            organization_id=row["organization_id"],
            user_id=row["user_id"],
            role=MembershipRole(row["role"]),
        )


class SQLiteReservationRepository:
    """SQLite reservation repository."""

    def __init__(
        self,
        db_path: str | None = None,
        connection: sqlite3.Connection | None = None,
    ) -> None:
        if db_path is not None and connection is not None:
            raise ValueError("Provide either db_path or connection, not both.")
        if connection is None:
            connection = sqlite3.connect(db_path or ":memory:", check_same_thread=False)
        connection.row_factory = sqlite3.Row
        self._connection = connection
        with self._connection:
            self._ensure_schema()

    def add(self, reservation: Reservation) -> None:
        with self._connection:
            self._connection.execute(
                """
                INSERT OR REPLACE INTO reservations (
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
                    reservation.status.value,
                ),
            )

    def get_by_id(self, reservation_id: str) -> Reservation | None:
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
            return None
        return self._row_to_reservation(row)

    def list_by_org(self, organization_id: str) -> list[Reservation]:
        rows = self._connection.execute(
            """
            SELECT id, organization_id, resource_id, starts_at_utc, ends_at_utc,
                   timezone, economic_value, status
            FROM reservations
            WHERE organization_id = ?
            ORDER BY id
            """,
            (organization_id,),
        ).fetchall()
        return [self._row_to_reservation(row) for row in rows]

    def list_by_resource(
        self, organization_id: str, resource_id: str
    ) -> list[Reservation]:
        rows = self._connection.execute(
            """
            SELECT id, organization_id, resource_id, starts_at_utc, ends_at_utc,
                   timezone, economic_value, status
            FROM reservations
            WHERE organization_id = ? AND resource_id = ?
            ORDER BY id
            """,
            (organization_id, resource_id),
        ).fetchall()
        return [self._row_to_reservation(row) for row in rows]

    def list_overlapping(
        self,
        organization_id: str,
        resource_id: str,
        starts_at_utc: datetime,
        ends_at_utc: datetime,
    ) -> list[Reservation]:
        rows = self._connection.execute(
            """
            SELECT id, organization_id, resource_id, starts_at_utc, ends_at_utc,
                   timezone, economic_value, status
            FROM reservations
            WHERE organization_id = ?
              AND resource_id = ?
              AND starts_at_utc < ?
              AND ends_at_utc > ?
            ORDER BY starts_at_utc, id
            """,
            (
                organization_id,
                resource_id,
                ends_at_utc.isoformat(),
                starts_at_utc.isoformat(),
            ),
        ).fetchall()
        return [self._row_to_reservation(row) for row in rows]

    def _ensure_schema(self) -> None:
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

    @staticmethod
    def _row_to_reservation(row: sqlite3.Row) -> Reservation:
        return Reservation(
            id=row["id"],
            organization_id=row["organization_id"],
            resource_id=row["resource_id"],
            starts_at_utc=datetime.fromisoformat(row["starts_at_utc"]),
            ends_at_utc=datetime.fromisoformat(row["ends_at_utc"]),
            timezone=row["timezone"],
            economic_value=row["economic_value"],
            status=ReservationStatus(row["status"]),
        )
