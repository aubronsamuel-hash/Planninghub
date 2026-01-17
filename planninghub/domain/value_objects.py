"""Value objects for PlanningHub."""

from enum import Enum


class MembershipRole(str, Enum):
    """Membership role values."""

    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class ResourceType(str, Enum):
    """Resource type values."""

    HUMAN = "human"
    ASSET = "asset"
    SERVICE = "service"


class ShiftStatus(str, Enum):
    """Shift status values."""

    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VALIDATED = "validated"
    CLOSED = "closed"


class ReservationStatus(str, Enum):
    """Reservation status values."""

    DRAFT = "draft"
    ACTIVE = "active"
    CANCELLED = "cancelled"


class ConflictSeverity(str, Enum):
    """Conflict severity values."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
