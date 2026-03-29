"""
Test script for ClawDev framework.

This script tests the basic functionality of the ClawDev framework
without actually connecting to an OpenClaw agent.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from clawdev.env.env import ChatEnv
from clawdev.phases.simple_phase import SimplePhase


class MockAgentAdapter:
    """Mock adapter for testing without real agent."""

    def send(self, message, role="default"):
        """Mock send method that returns a simple response."""
        return "Mock response with <result>test</result>"


def test_basic_functionality():
    """Test basic functionality of ClawDev framework."""
    adapter = MockAgentAdapter()

    env = ChatEnv("/tmp/test_project")
    env.task_prompt = "Create a simple calculator app"
    env.modality = "Application"
    env.language = "Python"

    print("Test completed successfully!")


if __name__ == "__main__":
    test_basic_functionality()
