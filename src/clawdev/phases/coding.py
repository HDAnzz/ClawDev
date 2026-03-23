"""
Coding Phase for ClawDev framework.

Generates initial code implementation based on requirements.
"""

from typing import Dict, Any
from ..phases.base import Phase


class CodingPhase(Phase):
    """Phase for generating initial code implementation."""

    def __init__(self, phase_config: Dict[str, Any]):
        super().__init__(phase_config)


class CodeCompletePhase(Phase):
    """Phase for completing unimplemented code sections."""

    def __init__(self, phase_config: Dict[str, Any]):
        super().__init__(phase_config)
