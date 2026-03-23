"""
Base phase class for ClawDev framework.

Defines the abstract interface and common functionality for all development phases.
"""

import logging
from typing import Dict, Any
from ..env.env import ChatEnv

logger = logging.getLogger(__name__)


class Phase:
    """Base class for all development phases."""

    def render_prompt(self, env: ChatEnv) -> str:
        """Render prompt for backward compatibility. Returns initiator prompt."""
        return self.render_initiator_prompt(env)

    def __init__(self, phase_config: Dict[str, Any]):
        """
        Initialize phase with configuration.

        Args:
            phase_config: Configuration dictionary for this phase
        """
        self.phase_config = phase_config
        self.phase_name = phase_config.get("phase", self.__class__.__name__)
        self.assistant_role = phase_config.get("assistant_role_name", "")
        self.user_role = phase_config.get("user_role_name", "")
        self.max_dialog_turns = phase_config.get("max_dialog_turns", 5)
        self.dialog_turn = 0

    def execute(self, env: ChatEnv, agent_adapter) -> ChatEnv:
        """
        Execute this phase as a dialog between two agents.

        The user_role agent initiates the conversation, and assistant_role responds.
        Since the backend has memory, we don't pass conversation history.

        Args:
            env: Current development environment
            agent_adapter: Adapter for communicating with AI agents

        Returns:
            Updated environment after dialog execution
        """
        logger.debug("[Phase] execute() phase=%s", self.phase_name)
        self.dialog_turn = 0

        initiator_prompt = self.render_initiator_prompt(env)
        logger.debug(
            "[Phase] initiator_prompt() returned %d chars", len(initiator_prompt)
        )

        response = agent_adapter.send(initiator_prompt, role=self.user_role)
        logger.debug("[Phase] initiator_response returned %d chars", len(response))

        if self._should_end_dialog(response):
            self.update_env(env, response)
            return env

        self.dialog_turn += 1
        other_role = self.user_role
        dialog_prompt = self.render_dialog_prompt(other_role, response)
        response = agent_adapter.send(dialog_prompt, role=self.assistant_role)
        logger.debug("[Phase] responder_response returned %d chars", len(response))

        if self._should_end_dialog(response):
            self.update_env(env, response)
            return env

        self.dialog_turn += 1

        while self.dialog_turn < self.max_dialog_turns:
            other_role = self.user_role
            dialog_prompt = self.render_dialog_prompt(other_role, response)
            response = agent_adapter.send(dialog_prompt, role=self.user_role)
            logger.debug(
                "[Phase] continuation response returned %d chars", len(response)
            )

            if self._should_end_dialog(response):
                break

            self.dialog_turn += 1
            other_role = self.assistant_role
            dialog_prompt = self.render_dialog_prompt(other_role, response)
            response = agent_adapter.send(dialog_prompt, role=self.assistant_role)
            logger.debug(
                "[Phase] continuation response returned %d chars", len(response)
            )

            if self._should_end_dialog(response):
                break

            self.dialog_turn += 1

        self.update_env(env, response)
        return env

    def render_initiator_prompt(self, env: ChatEnv) -> str:
        """Render the instruction for initiating the dialog."""
        initiator_prompt = self.phase_config.get("initiator_prompt", [])
        prompt_template = "\n".join(initiator_prompt)

        context = self.phase_config.get("context", "")
        context = self._format_prompt(context, env)

        return prompt_template.format(
            phase_name=self.phase_name,
            context=context,
            the_other_role=self.assistant_role,
            assistant_role=self.assistant_role,
            user_role=self.user_role,
        )

    def _get_phase_context(self, env: ChatEnv) -> str:
        """Get the phase-specific context based on current phase."""
        if self.phase_name == "DemandAnalysis":
            return f'User requirement: "{env.task_prompt}"'
        elif self.phase_name == "LanguageChoose":
            return f'User requirement: "{env.task_prompt}"\nProduct modality: "{env.modality}"'
        elif self.phase_name == "Coding":
            return f'User requirement: "{env.task_prompt}"\nDescription: "{env.description}"\nModality: "{env.modality}"\nLanguage: "{env.language}"'
        elif self.phase_name == "CodeComplete":
            return f'User requirement: "{env.task_prompt}"\nLanguage: "{env.language}"\nUnimplemented: "{env.unimplemented_file}"'
        elif self.phase_name == "CodeReviewComment":
            return f'User requirement: "{env.task_prompt}"\nLanguage: "{env.language}"'
        elif self.phase_name == "CodeReviewModification":
            return f'Language: "{env.language}"\nComments: "{env.comments}"'
        elif self.phase_name == "TestErrorSummary":
            return f'Language: "{env.language}"\nTest reports: "{env.test_reports}"'
        elif self.phase_name == "TestModification":
            return f'Language: "{env.language}"\nError summary: "{env.error_summary}"'
        elif self.phase_name == "EnvironmentDoc":
            return f'Language: "{env.language}"'
        elif self.phase_name == "Manual":
            return f'User requirement: "{env.task_prompt}"\nModality: "{env.modality}"\nLanguage: "{env.language}"'
        elif self.phase_name == "ArtDesign":
            return f'User requirement: "{env.task_prompt}"\nLanguage: "{env.language}"'
        elif self.phase_name == "ArtIntegration":
            return f'User requirement: "{env.task_prompt}"\nLanguage: "{env.language}"\nImages: "{env.images}"'
        return ""

    def render_dialog_prompt(self, the_other_role: str, content: str) -> str:
        """Render the dialog prompt with the other role's message."""
        prompt_template = self.phase_config.get(
            "dialog_prompt",
            "{the_other_role} said: {content}",
        )
        return prompt_template.format(the_other_role=the_other_role, content=content)

    def _should_end_dialog(self, response: str) -> bool:
        """Check if the dialog should end."""
        import re

        result_pattern = r"<result>\s*(.+?)\s*</result>"
        match = re.search(result_pattern, response, re.DOTALL)
        return match is not None

    def _format_prompt(self, prompt_template: str, env: ChatEnv) -> str:
        """Format prompt template with environment data."""
        try:
            return prompt_template.format(
                task=env.task_prompt,
                modality=env.modality,
                language=env.language,
                ideas=env.ideas,
                codes=env.get_codes(),
                requirements=env.requirements,
                comments=env.review_comments,
                test_reports=env.test_reports,
                error_summary=env.error_summary,
                images=env.images,
                unimplemented_file=env.unimplemented_file,
                description=env.description,
                gui=env.gui,
                assistant_role=self.assistant_role,
                user_role=self.user_role,
            )
        except KeyError as e:
            print(f"KeyError in _format_prompt: {e}")
            raise

    def update_env(self, env: ChatEnv, response: str) -> None:
        """Update environment based on agent response."""
        print(f"update_env: response={response}")
        import re

        result_pattern = r"<result>\s*(.+?)\s*</result>"
        match = re.search(result_pattern, response, re.DOTALL)
        if match:
            result_content = match.group(1).strip()
            print(f"update_env: result_content={result_content}")

            if self.phase_name == "DemandAnalysis":
                env.modality = result_content
            elif self.phase_name == "LanguageChoose":
                env.language = result_content
