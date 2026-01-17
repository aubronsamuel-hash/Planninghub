from planninghub.domain.services.conflict_outcomes import (
    ResolutionOutcomeType,
    resolve_outcome,
)
from planninghub.domain.services.conflict_resolution import ResolutionProposal


def test_resolve_outcome_manual_review() -> None:
    proposal = ResolutionProposal(
        reservation_id="res-1",
        strategy_id="noop",
        action="suggest_manual_review",
        details={"reason": "overlap"},
    )

    outcome = resolve_outcome(proposal)

    assert outcome is not None
    assert outcome.reservation_id == "res-1"
    assert outcome.outcome is ResolutionOutcomeType.NEEDS_MANUAL_REVIEW


def test_resolve_outcome_none() -> None:
    assert resolve_outcome(None) is None


def test_resolve_outcome_unknown_action() -> None:
    proposal = ResolutionProposal(
        reservation_id="res-2",
        strategy_id="noop",
        action="unknown_action",
        details={},
    )

    outcome = resolve_outcome(proposal)

    assert outcome is not None
    assert outcome.outcome is ResolutionOutcomeType.NEEDS_MANUAL_REVIEW
    assert outcome.reason == "unknown_action"
