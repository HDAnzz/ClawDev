"""
Language Choose Phase for ClawDev framework.

Determines the programming language based on requirements and modality.
"""

from typing import Dict, Any
from ..phases.base import Phase


class LanguageChoosePhase(Phase):
    """Phase for choosing the appropriate programming language."""

    def __init__(self, phase_config: Dict[str, Any]):
        super().__init__(phase_config)
