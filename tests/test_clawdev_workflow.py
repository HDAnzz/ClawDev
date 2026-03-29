"""
Integration test for ClawDev full workflow.

This test simulates the execution of the default ClawDev workflow and verifies
that each phase sends the correct prompt to the correct agent.
"""

import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from clawdev.adapter.agent_adapter import AgentAdapter
from clawdev.env.env import ChatEnv


class WorkflowRecorder:
    """Record the complete workflow execution."""

    def __init__(self, agent_configs):
        self.agent_configs = agent_configs
        self.steps = []
        self.adapter = None

    def create_adapter(self):
        """Create adapter that records calls."""
        adapter = AgentAdapter(self.agent_configs)
        self.adapter = adapter

        # Wrap send method to record calls
        def recorded_send(message, role="default"):
            agent_name = adapter.agent_configs.get(role, "chief_executive_officer")
            self.steps.append(
                {
                    "role": role,
                    "agent_name": agent_name,
                    "message_preview": message[:200] if message else "",
                    "message_length": len(message),
                }
            )
            # Return mock response based on role
            return self._mock_response(role)

        adapter.send = recorded_send

        return adapter

    def _mock_response(self, role):
        """Return mock response based on role."""
        responses = {
            "Chief Product Officer": "Based on the task, I recommend we create an Application.\n<INFO> Application",
            "Chief Technology Officer": "For this task, Python would be the best choice.\n<INFO> Python",
            "Programmer": "Here is the code:\n\nmain.py\n```python\nprint('Hello')\n```\n<INFO> Code complete",
            "Code Reviewer": "Code looks good, no issues found.\n<INFO> Finished",
            "Software Test Engineer": "All tests passed.\n<INFO> No errors",
            "Chief Creative Officer": "Design approved.\n<INFO> Approved",
        }
        return responses.get(role, f"Mock response for {role}")


def load_chain_config():
    """Load chain configuration."""
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "configs", "default", "ChatChainConfig.json"
    )
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_phase_config():
    """Load phase configuration."""
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "configs", "default", "PhaseConfig.json"
    )
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def agent_configs():
    """Agent configuration mapping."""
    return {
        "Chief Executive Officer": "chief_executive_officer",
        "Chief Product Officer": "chief_product_officer",
        "Chief Technology Officer": "chief_technology_officer",
        "Programmer": "programmer",
        "Code Reviewer": "code_reviewer",
        "Software Test Engineer": "software_test_engineer",
        "Chief Creative Officer": "chief_creative_officer",
        "Counselor": "counselor",
        "Chief Human Resource Officer": "chief_human_resource_officer",
    }


@pytest.fixture
def chain_config():
    """Load chain config."""
    return load_chain_config()


@pytest.fixture
def phase_config():
    """Load phase config."""
    return load_phase_config()


class TestPhaseSequence:
    """Test individual phase execution sequence."""

    def test_demand_analysis_sends_to_ceo(self, agent_configs, phase_config):
        """Test that DemandAnalysis phase sends to CEO (user_role initiates)."""
        recorder = WorkflowRecorder(agent_configs)
        adapter = recorder.create_adapter()

        from clawdev.phases.simple_phase import SimplePhase

        # Create phase
        phase = SimplePhase(phase_config["DemandAnalysis"])

        # Create env
        env = ChatEnv("/tmp/test")
        env.task_prompt = "Create a calculator"

        # Execute
        env = phase.execute(env, adapter)

        # Verify first message goes to CEO (user_role, the initiator)
        assert len(recorder.steps) >= 1
        first_step = recorder.steps[0]
        assert first_step["role"] == "Chief Executive Officer"
        assert first_step["agent_name"] == "chief_executive_officer"

    def test_language_choose_sends_to_ceo(self, agent_configs, phase_config):
        """Test that LanguageChoose phase sends to CEO (user_role initiates)."""
        recorder = WorkflowRecorder(agent_configs)
        adapter = recorder.create_adapter()

        from clawdev.phases.simple_phase import SimplePhase

        phase = SimplePhase(phase_config["LanguageChoose"])

        env = ChatEnv("/tmp/test")
        env.task_prompt = "Create a calculator"
        env.modality = "Application"

        env = phase.execute(env, adapter)

        assert len(recorder.steps) >= 1
        first_step = recorder.steps[0]
        assert first_step["role"] == "Chief Executive Officer"
        assert first_step["agent_name"] == "chief_executive_officer"


class TestMessageContent:
    """Test that messages contain expected content."""

    def test_demand_analysis_prompt_contains_task(self, agent_configs, phase_config):
        """Test that DemandAnalysis prompt contains task information."""
        from clawdev.phases.simple_phase import SimplePhase

        adapter = AgentAdapter(agent_configs)

        # Override send to capture message
        captured_message = []

        def capture_send(message, role="default"):
            captured_message.append(message)
            return "Test response"

        adapter.send = capture_send

        phase = SimplePhase(phase_config["DemandAnalysis"])

        env = ChatEnv("/tmp/test")
        env.task_prompt = "Create a calculator app"

        phase.execute(env, adapter)

        assert len(captured_message) >= 1
        first_message = captured_message[0]

        # Verify prompt contains task
        assert (
            "Create a calculator app" in first_message
            or "calculator" in first_message.lower()
        ), "Prompt should contain task information"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
