"""
Demand Analysis Phase for ClawDev framework.

Determines the software product modality based on user requirements.
"""

from typing import Dict, Any
from ..phases.base import Phase


class DemandAnalysisPhase(Phase):
    """Phase for analyzing user requirements and determining product modality."""

    def __init__(self, phase_config: Dict[str, Any]):
        super().__init__(phase_config)
