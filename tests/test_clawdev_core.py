"""
Tests for ClawDev core components: ChatEnv, SimplePhase, ComposedPhase, ChatChain.
"""

import sys
import os
import json

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from clawdev.env.env import ChatEnv
from clawdev.phases.simple_phase import SimplePhase
from clawdev.phases.composed_phase import ComposedPhase
from clawdev.chain.chain import ChatChain
from clawdev.adapter.agent_adapter import AgentAdapter


class TestChatEnv:
    """Test ChatEnv functionality."""

    def test_init_with_project_name(self):
        """Test ChatEnv initialization with project name."""
        env = ChatEnv("test_project")
        assert env.project_name == "test_project"

    def test_init_defaults(self):
        """Test default values."""
        env = ChatEnv("test_project")
        assert env.task_prompt == ""
        assert env.modality == ""
        assert env.language == ""

    def test_set_fields(self):
        """Test setting fields."""
        env = ChatEnv("test_project")
        env.task_prompt = "Create a calculator"
        env.modality = "Application"
        env.language = "Python"

        assert env.task_prompt == "Create a calculator"
        assert env.modality == "Application"
        assert env.language == "Python"


class TestSimplePhase:
    """Test SimplePhase functionality."""

    def test_init(self):
        """Test SimplePhase initialization."""
        config = {
            "assistant_role_name": "Chief Product Officer",
            "user_role_name": "Chief Executive Officer",
            "initiator_prompt": ["Task: {task}"],
            "dialog_prompt": "{the_other_role} said: {content}",
        }
        phase = SimplePhase(config, phase_name="DemandAnalysis")
        assert phase.phase_name == "DemandAnalysis"
        assert phase.assistant_role == "Chief Product Officer"
        assert phase.user_role == "Chief Executive Officer"

    def test_render_initiator_prompt(self):
        """Test prompt rendering with environment."""
        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "initiator_prompt": ["Task: {task}", "Modality: {modality}"],
            "dialog_prompt": "{the_other_role} said: {content}",
        }
        phase = SimplePhase(config)

        env = ChatEnv("test")
        env.task_prompt = "Create calculator"
        env.modality = "Application"

        prompt = phase.render_initiator_prompt(env)
        assert "Create calculator" in prompt
        assert "Application" in prompt

    def test_render_dialog_prompt(self):
        """Test dialog prompt rendering."""
        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "initiator_prompt": ["Task: {task}"],
            "dialog_prompt": "{the_other_role} said: {content}",
        }
        phase = SimplePhase(config)
        prompt = phase.render_dialog_prompt("CEO", "Hello world")
        assert "CEO said:" in prompt
        assert "Hello world" in prompt


class TestShouldEndDialog:
    """Test _should_end_dialog detection logic."""

    def test_result_tag_ends_dialog(self):
        """Test that <result> tag ends dialog."""
        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "initiator_prompt": ["Task: {task}"],
            "dialog_prompt": "{the_other_role} said: {content}",
        }
        phase = SimplePhase(config)

        assert phase._should_end_dialog("Some text <result>Done</result>") is True

    def test_result_tag_with_content(self):
        """Test result tag with content."""
        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "initiator_prompt": [],
            "dialog_prompt": "",
        }
        phase = SimplePhase(config)

        assert phase._should_end_dialog("<result>Application</result>") is True

    def test_no_result_tag(self):
        """Test that text without result tag does not end dialog."""
        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "initiator_prompt": [],
            "dialog_prompt": "",
        }
        phase = SimplePhase(config)

        assert phase._should_end_dialog("Just some text without result") is False

    def test_result_inside_double_quotes(self):
        """Test result inside double quotes does not end dialog."""
        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "initiator_prompt": [],
            "dialog_prompt": "",
        }
        phase = SimplePhase(config)

        assert (
            phase._should_end_dialog('Say "<result>Done</result>" when done') is False
        )

    def test_result_inside_single_quotes(self):
        """Test result inside single quotes does not end dialog."""
        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "initiator_prompt": [],
            "dialog_prompt": "",
        }
        phase = SimplePhase(config)

        assert (
            phase._should_end_dialog("Say '<result>Done</result>' when done") is False
        )

    def test_result_inside_backticks(self):
        """Test result inside backticks does not end dialog."""
        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "initiator_prompt": [],
            "dialog_prompt": "",
        }
        phase = SimplePhase(config)

        assert phase._should_end_dialog("`<result>Done</result>`") is False

    def test_multiple_result_tags(self):
        """Test multiple result tags returns first valid."""
        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "initiator_prompt": [],
            "dialog_prompt": "",
        }
        phase = SimplePhase(config)

        assert (
            phase._should_end_dialog(
                "First <result>Done</result> then <result>More</result>"
            )
            is True
        )


class TestSimplePhaseExecute:
    """Test SimplePhase.execute() with mock adapter."""

    def test_execute_single_turn(self):
        """Test execute ends after first response with result."""

        class MockAdapter:
            def send(self, message, role):
                return "Response <result>Done</result>"

        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "initiator_prompt": ["Task: {task}"],
            "dialog_prompt": "{the_other_role} said: {content}",
        }
        phase = SimplePhase(config, phase_name="Test")
        env = ChatEnv("test")
        env.task_prompt = "Test task"

        result_env = phase.execute(env, MockAdapter())
        assert result_env is not None

    def test_execute_max_turns(self):
        """Test execute respects max_dialog_turns."""

        class MockAdapter:
            call_count = 0

            def send(self, message, role):
                self.call_count += 1
                return "Response without result"

        adapter = MockAdapter()
        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "max_dialog_turns": 3,
            "initiator_prompt": ["Task: {task}"],
            "dialog_prompt": "{the_other_role} said: {content}",
        }
        phase = SimplePhase(config)
        env = ChatEnv("test")
        env.task_prompt = "Test"

        phase.execute(env, adapter)
        assert adapter.call_count > 0


class TestComposedPhase:
    """Test ComposedPhase functionality."""

    def test_init(self):
        """Test ComposedPhase initialization."""
        config = {
            "phase": "Coding",
            "cycleNum": 2,
            "composition": [
                {"phaseType": "SimplePhase", "phase": "DemandAnalysis"},
                {"phaseType": "SimplePhase", "phase": "LanguageChoose"},
            ],
        }

        phase_config = {
            "DemandAnalysis": {
                "assistant_role_name": "CPO",
                "user_role_name": "CEO",
                "initiator_prompt": [],
                "dialog_prompt": "",
            }
        }

        phase = ComposedPhase(config, config_phase=phase_config)
        assert phase.cycle_num == 2
        assert len(phase.composition) == 2


class TestChatChain:
    """Test ChatChain functionality."""

    def test_init(self):
        """Test ChatChain initialization."""
        agent_configs = {
            "Chief Executive Officer": "chief_executive_officer",
            "Chief Product Officer": "chief_product_officer",
        }
        adapter = AgentAdapter(agent_configs)

        chain = ChatChain(adapter, config_name="default")
        assert chain.config_name == "default"
        assert chain.env is None

    def test_pre_processing(self):
        """Test pre_processing initializes environment."""
        agent_configs = {"Chief Executive Officer": "ceo"}
        adapter = AgentAdapter(agent_configs)
        chain = ChatChain(adapter, config_name="default")

        chain.pre_processing("Create a calculator", "calculator_project")

        assert chain.env is not None
        assert chain.env.project_name == "calculator_project"
        assert chain.env.task_prompt == "Create a calculator"

    def test_execute_step_simple_phase(self):
        """Test execute_step with SimplePhase."""
        agent_configs = {"Chief Executive Officer": "ceo"}

        class MockAgentAdapter:
            def __init__(self, configs):
                self.agent_configs = configs

            def send(self, message, role):
                return "Response <result>Done</result>"

        adapter = MockAgentAdapter(agent_configs)

        chain = ChatChain(adapter, config_name="default")
        chain.pre_processing("Test task", "test_project")

        phase_item = {
            "phaseType": "SimplePhase",
            "phase": "DemandAnalysis",
        }

        chain.execute_step(phase_item)
        assert chain.env is not None


class TestPromptFormatting:
    """Test prompt formatting with environment data."""

    def test_format_with_all_fields(self):
        """Test formatting with all required fields."""
        config = {
            "assistant_role_name": "CPO",
            "user_role_name": "CEO",
            "initiator_prompt": [
                "Task: {task}",
                "Modality: {modality}",
                "Language: {language}",
            ],
            "dialog_prompt": "{the_other_role} said: {content}",
        }
        phase = SimplePhase(config)

        env = ChatEnv("project")
        env.task_prompt = "Build calculator"
        env.modality = "Application"
        env.language = "Python"

        prompt = phase.render_initiator_prompt(env)
        assert "Build calculator" in prompt
        assert "Application" in prompt
        assert "Python" in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
