from planninghub.domain.services.conflict_detection import ConflictCandidate
from planninghub.domain.services.conflict_resolution import NoopResolutionStrategy
from planninghub.domain.value_objects import ConflictSeverity


def test_noop_resolution_strategy_proposes_manual_review() -> None:
    candidate = ConflictCandidate(
        reservation_id="res-1",
        resource_id="resource-1",
        overlapping_reservation_ids=["res-2", "res-3"],
        severity=ConflictSeverity.HIGH,
        reason="overlapping_reservations",
    )

    proposal = NoopResolutionStrategy().propose(candidate)

    assert proposal is not None
    assert proposal.reservation_id == "res-1"
    assert proposal.strategy_id == "noop"
    assert proposal.action == "suggest_manual_review"
    assert proposal.details["overlap_count"] == "2"
    assert proposal.details["reason"] == candidate.reason
