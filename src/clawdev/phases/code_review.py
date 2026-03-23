"""
Code Review Phase for ClawDev framework.

Reviews and improves code quality through automated feedback.
"""

from typing import Dict, Any
from ..phases.base import Phase


class CodeReviewCommentPhase(Phase):
    """Phase for generating code review comments."""

    def __init__(self, phase_config: Dict[str, Any]):
        super().__init__(phase_config)


class CodeReviewModificationPhase(Phase):
    """Phase for modifying code based on review comments."""

    def __init__(self, phase_config: Dict[str, Any]):
        super().__init__(phase_config)
