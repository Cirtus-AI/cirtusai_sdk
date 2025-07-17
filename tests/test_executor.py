
import pytest
from unittest.mock import MagicMock, patch
from langchain.agents import AgentExecutor
from cirtusai.executor import create_agent_executor
from cirtusai.agent import CirtusAgent

@pytest.fixture
def mock_cirtus_agent():
    """Create a mock CirtusAgent object."""
    agent = MagicMock(spec=CirtusAgent)
    agent.list_master_agent.return_value = {"status": "master agent ok"}
    agent.list_assets.return_value = {"status": "assets ok"}
    agent.provision_email.return_value = {"status": "email provisioned"}
    agent.provision_wallet.return_value = {"status": "wallet provisioned"}
    agent.command.return_value = {"status": "command ok"}
    agent.list_email_accounts.return_value = [{"email": "test@example.com"}]
    agent.create_email_account.return_value = {"status": "email account created"}
    agent.issue_credential.return_value = {"status": "credential issued"}
    return agent

@patch('cirtusai.executor.ChatDeepSeek')
@patch('cirtusai.executor.create_openai_tools_agent')
@patch('cirtusai.executor.AgentExecutor')
def test_create_agent_executor(MockAgentExecutor, mock_create_agent, mock_chat_deepseek, mock_cirtus_agent):
    """
    Test that the create_agent_executor function returns a valid AgentExecutor
    and that its tools correctly call the CirtusAgent methods.
    """
    # Arrange
    dummy_api_key = "sk-testkey"
    mock_agent_instance = MagicMock()
    mock_create_agent.return_value = mock_agent_instance

    # Act
    executor = create_agent_executor(mock_cirtus_agent, dummy_api_key)

    # Assert
    # Check that ChatDeepSeek was called correctly
    mock_chat_deepseek.assert_called_once_with(model="deepseek-chat", api_key=dummy_api_key, temperature=0)

    # Check that create_openai_tools_agent was called
    assert mock_create_agent.called
    
    # Check that AgentExecutor was initialized
    MockAgentExecutor.assert_called_once_with(agent=mock_agent_instance, tools=mock_create_agent.call_args[0][1], verbose=True)

    # Check that the returned object is the one from AgentExecutor
    assert executor == MockAgentExecutor.return_value

    # Now, let's inspect the tools that were passed to create_openai_tools_agent
    tools = mock_create_agent.call_args[0][1]
    tool_map = {tool.name: tool for tool in tools}

    # Verify a few tools to ensure they are wired up correctly
    # Test 'list_master_agent' tool
    assert tool_map['list_master_agent'].func() == {"status": "master agent ok"}
    mock_cirtus_agent.list_master_agent.assert_called_once()

    # Test 'provision_wallet' tool
    assert tool_map['provision_wallet'].func(chain="solana") == {"status": "wallet provisioned"}
    mock_cirtus_agent.provision_wallet.assert_called_once_with("solana")

    # Test 'command' tool
    assert tool_map['command'].func(text="do something") == {"status": "command ok"}
    mock_cirtus_agent.command.assert_called_once_with("do something")
