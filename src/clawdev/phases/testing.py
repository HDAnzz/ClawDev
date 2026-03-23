"""
Testing Phase for ClawDev framework.

Tests and fixes code based on error reports.
"""

from typing import Dict, Any
from ..phases.base import Phase


class TestErrorSummaryPhase(Phase):
    """Phase for summarizing test errors."""

    def __init__(self, phase_config: Dict[str, Any]):
        super().__init__(phase_config)


class TestModificationPhase(Phase):
    """Phase for modifying code based on test errors."""

    def __init__(self, phase_config: Dict[str, Any]):
        super().__init__(phase_config)
