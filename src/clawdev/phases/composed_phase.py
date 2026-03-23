"""
Composed Phase for ClawDev framework.

Executes multiple phases in a loop with configurable cycle limits.
"""

from typing import Dict, Any
from ..phases.base import Phase


class ComposedPhase(Phase):
    """Phase that executes multiple sub-phases in a loop."""

    def __init__(self, phase_config: Dict[str, Any]):
        super().__init__(phase_config)
        self.cycle_num = phase_config.get("cycleNum", 1)
        self.composition = phase_config.get("Composition", [])
