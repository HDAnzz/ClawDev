"""
Agent adapter for ClawDev framework.

Provides a unified interface for communicating with AI agents through OpenClaw ACP.
"""

from typing import Dict, Any, Optional
from openclaw_acp import OpenClawAgent


class AgentAdapter:
    """Adapter that wraps OpenClawAgent for use in ClawDev framework."""

    def __init__(self, agent: OpenClawAgent):
        """
        Initialize adapter with OpenClaw agent.

        Args:
            agent: OpenClawAgent instance to wrap
        """
        self.agent = agent

    def send(self, message: str) -> str:
        """
        Send message to agent and get response.

        Args:
            message: Message to send to agent

        Returns:
            Agent's response
        """
        return self.agent.step(message)

    def reset(self) -> None:
        """Reset agent session."""
        # Implementation depends on how OpenClawAgent handles resets
        # This might involve stopping and restarting the agent
        pass
