import os
import pytest
from unittest.mock import Mock, patch

from openclaw_acp.agent import OpenClawAgent


class TestOpenClawAgent:
    @patch.dict("os.environ", {"OPENCLAW_GATEWAY_TOKEN": "test_token"})
    def test_default_gateway_url(self):
        agent = OpenClawAgent(auto_start=False)
        assert agent.gateway_url == "ws://127.0.0.1:18789"

    @patch.dict("os.environ", {"OPENCLAW_GATEWAY_TOKEN": "test_token"})
    def test_custom_gateway_url(self):
        agent = OpenClawAgent(gateway_url="ws://custom:9999", auto_start=False)
        assert agent.gateway_url == "ws://custom:9999"

    @patch.dict("os.environ", {"OPENCLAW_GATEWAY_TOKEN": "test_token"})
    def test_default_agent_name(self):
        agent = OpenClawAgent(auto_start=False)
        assert agent.agent == "main"

    @patch.dict("os.environ", {"OPENCLAW_GATEWAY_TOKEN": "test_token"})
    def test_custom_agent_name(self):
        agent = OpenClawAgent(agent="custom_agent", auto_start=False)
        assert agent.agent == "custom_agent"

    @patch.dict("os.environ", {"OPENCLAW_GATEWAY_TOKEN": "test_token"})
    def test_not_started_by_default(self):
        agent = OpenClawAgent(auto_start=False)
        assert agent._started is False

    @patch.dict("os.environ", {"OPENCLAW_GATEWAY_TOKEN": "test_token"})
    def test_initial_state(self):
        agent = OpenClawAgent(auto_start=False)
        assert agent._proc is None
        assert agent._session_id is None
        assert agent._pending == {}

    @patch.dict("os.environ", {"OPENCLAW_GATEWAY_TOKEN": "test_token"})
    def test_step_raises_when_not_started(self):
        agent = OpenClawAgent(auto_start=False)
        with pytest.raises(RuntimeError, match="请先调用 start()"):
            agent.step("test message")

    @patch.dict("os.environ", {"OPENCLAW_GATEWAY_TOKEN": "test_token"})
    def test_call_forwards_to_step(self):
        agent = OpenClawAgent(auto_start=False)
        agent.step = Mock(return_value="response")
        result = agent("test message")
        agent.step.assert_called_once_with("test message", 120)
        assert result == "response"

    @patch.dict("os.environ", {"OPENCLAW_GATEWAY_TOKEN": "test_token"})
    def test_context_manager(self):
        with patch.object(OpenClawAgent, "start") as mock_start:
            with OpenClawAgent(auto_start=False):
                mock_start.assert_called_once()

    @patch.dict("os.environ", {"OPENCLAW_GATEWAY_TOKEN": "test_token"})
    def test_context_manager_stops_on_exit(self):
        with patch.object(OpenClawAgent, "start"):
            with patch.object(OpenClawAgent, "stop") as mock_stop:
                agent = OpenClawAgent(auto_start=False)
                agent.stop()
                mock_stop.assert_called_once()


class TestOpenClawAgentRequiresApiKey:
    def test_raises_without_token(self):
        with pytest.raises(ValueError, match="API key"):
            OpenClawAgent(auto_start=False)

    def test_accepts_token_in_env(self):
        with patch.dict(os.environ, {"OPENCLAW_GATEWAY_TOKEN": "test_token"}):
            agent = OpenClawAgent(auto_start=False)
            assert agent is not None
