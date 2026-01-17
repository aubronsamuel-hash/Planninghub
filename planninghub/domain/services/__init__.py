"""Domain services for PlanningHub."""

from planninghub.domain.services.conflict_detection import (
    ConflictCandidate,
    ConflictDetectionService,
)
from planninghub.domain.services.conflict_orchestrator import (
    ConflictOrchestrator,
    OrchestrationResult,
)
from planninghub.domain.services.conflict_outcomes import (
    ResolutionOutcome,
    ResolutionOutcomeType,
    resolve_outcome,
)
from planninghub.domain.services.conflict_resolution import (
    ConflictResolutionStrategy,
    NoopResolutionStrategy,
    ResolutionProposal,
)

__all__ = [
    "ConflictCandidate",
    "ConflictDetectionService",
    "ConflictOrchestrator",
    "ConflictResolutionStrategy",
    "NoopResolutionStrategy",
    "OrchestrationResult",
    "ResolutionOutcome",
    "ResolutionOutcomeType",
    "ResolutionProposal",
    "resolve_outcome",
]
