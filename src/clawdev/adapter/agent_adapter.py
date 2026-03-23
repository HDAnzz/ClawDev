"""
Agent adapter for ClawDev framework.

Provides a unified interface for communicating with AI agents through OpenClaw ACP.
"""

import logging
from typing import Dict, Optional, List
from openclaw_acp import OpenClawAgent

logger = logging.getLogger(__name__)


class ConversationHistory:
    """Manages conversation history for a dialog between two agents."""

    def __init__(self):
        """Initialize empty conversation history."""
        self.messages: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history.

        Args:
            role: Role name of the message sender
            content: Message content
        """
        self.messages.append({"role": role, "content": content})

    def get_history_text(self) -> str:
        """
        Get conversation history as formatted text.

        Returns:
            Formatted conversation history
        """
        if not self.messages:
            return ""
        history_lines = []
        for i, msg in enumerate(self.messages):
            role_label = msg["role"]
            content = msg["content"]
            history_lines.append(f"[{i}] {role_label}: {content}")
        return "\n".join(history_lines)

    def clear(self) -> None:
        """Clear conversation history."""
        self.messages.clear()


class AgentAdapter:
    """Adapter that wraps OpenClawAgent for use in ClawDev framework."""

    def __init__(self, agent_configs: Dict[str, str]):
        """
        Initialize adapter with OpenClaw agent configurations.

        Args:
            agent_configs: Dictionary mapping role names to agent names
                           e.g., {"Chief Executive Officer": "chief_executive_officer"}
        """
        self.agent_configs = agent_configs
        self.agents: Dict[str, OpenClawAgent] = {}
        self.conversation_histories: Dict[str, ConversationHistory] = {}
        self._session_contexts: Dict[str, str] = {}

    def set_session_context(self, role: str, context: str) -> None:
        """
        Set session context for an agent role.

        Args:
            role: Role name
            context: Context message to send after agent initialization
        """
        self._session_contexts[role] = context

    def get_agent(self, role: str) -> OpenClawAgent:
        """
        Get or create an agent for the specified role.

        Args:
            role: Role name to determine which agent to use

        Returns:
            OpenClawAgent instance
        """
        agent_name = self.agent_configs.get(role, "default")
        if agent_name not in self.agents:
            logger.debug("[AgentAdapter] Creating new agent: %s", agent_name)
            session_context = self._session_contexts.get(role)
            self.agents[agent_name] = OpenClawAgent(
                agent=agent_name,
                session_context=session_context,
            )
        return self.agents[agent_name]

    def get_conversation_history(self, dialog_id: str) -> ConversationHistory:
        """
        Get or create conversation history for a dialog.

        Args:
            dialog_id: Unique identifier for the dialog

        Returns:
            ConversationHistory instance
        """
        if dialog_id not in self.conversation_histories:
            self.conversation_histories[dialog_id] = ConversationHistory()
        return self.conversation_histories[dialog_id]

    def send(
        self,
        message: str,
        role: str = "default",
        dialog_id: Optional[str] = None,
        include_history: bool = True,
    ) -> str:
        """
        Send message to agent and get response.

        Args:
            message: Message to send to agent
            role: Role name to determine which agent to use
            dialog_id: Optional dialog ID for conversation history
            include_history: Whether to include conversation history in the message

        Returns:
            Agent's response
        """
        logger.debug(
            "[AgentAdapter] send() role=%s dialog_id=%s message=%r",
            role,
            dialog_id,
            message[:100] if message else "",
        )

        if dialog_id and include_history:
            history = self.get_conversation_history(dialog_id)
            history_text = history.get_history_text()
            if history_text:
                message = f"[Conversation History]\n{history_text}\n\n[Current Message]\n{message}"

        agent = self.get_agent(role)
        logger.debug("[AgentAdapter] Calling agent.step()")
        response = agent.step(message)
        logger.debug("[AgentAdapter] agent.step() returned %d chars", len(response))

        if dialog_id:
            history = self.get_conversation_history(dialog_id)
            history.add_message(role, message)
            history.add_message(role + "_response", response)

        return response

    def send_dialog(
        self,
        initiator_message: str,
        responder_message: str,
        initiator_role: str,
        responder_role: str,
        dialog_id: str,
    ) -> str:
        """
        Execute a dialog turn between two agents.

        Args:
            initiator_message: Initial message for the initiator
            responder_message: Prompt for the responder
            initiator_role: Role name for the initiator agent
            responder_role: Role name for the responder agent
            dialog_id: Unique identifier for the dialog

        Returns:
            Final response from the initiator after dialog
        """
        initiator_response = self.send(initiator_message, initiator_role, dialog_id)

        history = self.get_conversation_history(dialog_id)
        history_text = history.get_history_text()
        full_context = f"[Conversation History]\n{history_text}\n\n[Respond to this]\n{responder_message}"

        responder_response = self.send(full_context, responder_role, dialog_id)

        return initiator_response + "\n" + responder_response

    def reset_conversation_history(self, dialog_id: Optional[str] = None) -> None:
        """
        Reset conversation history.

        Args:
            dialog_id: If provided, reset only this dialog's history.
                      If None, reset all histories.
        """
        if dialog_id:
            if dialog_id in self.conversation_histories:
                self.conversation_histories[dialog_id].clear()
        else:
            for history in self.conversation_histories.values():
                history.clear()

    def reset(self) -> None:
        """Reset all agents and conversation histories."""
        for agent in self.agents.values():
            try:
                agent.stop()
            except Exception:
                pass
        self.agents.clear()
        self.conversation_histories.clear()
