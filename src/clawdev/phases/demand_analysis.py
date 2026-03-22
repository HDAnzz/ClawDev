"""
Demand Analysis Phase for ClawDev framework.

Determines the software product modality based on user requirements.
"""

from typing import Dict, Any
from ..phases.base import Phase
from ..env.env import ChatEnv


class DemandAnalysisPhase(Phase):
    """Phase for analyzing user requirements and determining product modality."""

    def __init__(self, phase_config: Dict[str, Any]):
        """
        Initialize demand analysis phase.

        Args:
            phase_config: Configuration for this phase
        """
        super().__init__(phase_config)

    def execute(self, env: ChatEnv, agent_adapter) -> ChatEnv:
        """
        Execute demand analysis phase.

        Args:
            env: Current development environment
            agent_adapter: Adapter for communicating with AI agents

        Returns:
            Updated environment with determined modality
        """
        # Render prompt for this phase
        prompt = self.render_prompt(env)

        # Send prompt to agent and get response
        response = agent_adapter.send(prompt)

        # Update environment with agent response
        self.update_env(env, response)

        return env
