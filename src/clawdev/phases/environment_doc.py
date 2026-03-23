"""
Environment Documentation Phase for ClawDev framework.

Generates environment documentation and requirements files.
"""

from typing import Dict, Any
from ..phases.base import Phase


class EnvironmentDocPhase(Phase):
    """Phase for generating environment documentation."""

    def __init__(self, phase_config: Dict[str, Any]):
        super().__init__(phase_config)


class ManualPhase(Phase):
    """Phase for generating user manuals."""

    def __init__(self, phase_config: Dict[str, Any]):
        super().__init__(phase_config)
