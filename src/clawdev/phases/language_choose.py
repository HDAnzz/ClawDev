"""
Language Choose Phase for ClawDev framework.

Determines the programming language based on requirements and modality.
"""

from typing import Dict, Any
from ..phases.base import Phase
from ..env.env import ChatEnv


class LanguageChoosePhase(Phase):
    """Phase for choosing the appropriate programming language."""

    def __init__(self, phase_config: Dict[str, Any]):
        """
        Initialize language choose phase.

        Args:
            phase_config: Configuration for this phase
        """
        super().__init__(phase_config)

    def execute(self, env: ChatEnv, agent_adapter) -> ChatEnv:
        """
        Execute language choose phase.

        Args:
            env: Current development environment
            agent_adapter: Adapter for communicating with AI agents

        Returns:
            Updated environment with chosen language
        """
        # Render prompt for this phase
        prompt = self.render_prompt(env)

        # Send prompt to agent and get response
        response = agent_adapter.send(prompt)

        # Update environment with agent response
        self.update_env(env, response)

        return env
