"""CLI adapter for evaluating incoming reservations."""

from __future__ import annotations

import sys
from datetime import datetime

from planninghub.application.handlers import EvaluateIncomingReservationHandler
from planninghub.application.ports import EvaluateIncomingReservationCommand
from planninghub.domain.entities import Reservation
from planninghub.domain.services.conflict_resolution import NoopResolutionStrategy
from planninghub.domain.value_objects import ReservationStatus
from planninghub.infra.repositories_in_memory import InMemoryReservationRepository

EXPECTED_ARGS = 5


def _build_seed_reservation(organization_id: str, resource_id: str) -> Reservation:
    return Reservation(
        id="res-1",
        organization_id=organization_id,
        resource_id=resource_id,
        starts_at_utc=datetime.fromisoformat("2024-01-01T08:00:00"),
        ends_at_utc=datetime.fromisoformat("2024-01-01T10:00:00"),
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )


def run_cli(args: list[str]) -> int:
    if len(args) != EXPECTED_ARGS:
        print("error=bad_args")
        return 2

    organization_id, reservation_id, resource_id, starts_at, ends_at = args
    try:
        starts_at_utc = datetime.fromisoformat(starts_at)
        ends_at_utc = datetime.fromisoformat(ends_at)
    except ValueError:
        print("error=parse_datetime")
        return 2

    reservation = Reservation(
        id=reservation_id,
        organization_id=organization_id,
        resource_id=resource_id,
        starts_at_utc=starts_at_utc,
        ends_at_utc=ends_at_utc,
        timezone="UTC",
        economic_value=None,
        status=ReservationStatus.ACTIVE,
    )

    repository = InMemoryReservationRepository()
    repository.add(_build_seed_reservation(organization_id, resource_id))

    handler = EvaluateIncomingReservationHandler(
        reservation_repo=repository,
        strategies=[NoopResolutionStrategy()],
    )
    response = handler.handle(
        EvaluateIncomingReservationCommand(
            organization_id=organization_id,
            reservation=reservation,
        )
    )

    if response.conflict is False:
        print("conflict=false")
        return 0

    severity = "high" if response.proposal is not None else "none"
    outcome = response.outcome.outcome.value if response.outcome else "none"
    overlaps = 0
    if response.proposal is not None:
        overlaps = int(response.proposal.details.get("overlap_count", "0"))
    print(
        "conflict=true severity={severity} outcome={outcome} overlaps={overlaps}".format(
            severity=severity,
            outcome=outcome,
            overlaps=overlaps,
        )
    )
    return 0


def main() -> None:
    code = run_cli(sys.argv[1:])
    raise SystemExit(code)


if __name__ == "__main__":
    main()
