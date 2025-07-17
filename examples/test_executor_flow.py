

import os
from unittest.mock import MagicMock
from dotenv import load_dotenv
from cirtusai.agent import CirtusAgent
from cirtusai.executor import create_agent_executor

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# IMPORTANT: Set your actual DeepSeek API key here or in your environment
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "YOUR_DEEPSEEK_API_KEY_HERE")
AGENT_ID = "test-agent-123"
TOKEN = "test-token"

# --- Mocking CirtusAgent for Local Testing ---
def get_mocked_cirtus_agent():
    """Creates a CirtusAgent with mocked methods to simulate API calls."""
    # Create a mock instance that still adheres to the CirtusAgent class spec
    mock_agent = MagicMock(spec=CirtusAgent)

    # Define return values for each tool the agent can use
    mock_agent.list_master_agent.return_value = {"id": "master-001", "name": "MasterAgent", "did": "did:key:z6Mkt..."}
    mock_agent.list_assets.return_value = {"wallets": [{"id": "w-123", "chain": "ethereum"}], "emails": [{"id": "e-456", "address": "test@example.com"}]}
    mock_agent.provision_email.return_value = {"status": "success", "asset_id": "e-789", "message": "Email provisioned."}
    mock_agent.provision_wallet.return_value = {"status": "success", "asset_id": "w-abc", "chain": "solana"}
    mock_agent.command.return_value = {"status": "received", "message_id": "msg-xyz"}
    mock_agent.list_email_accounts.return_value = [{"id": "e-456", "provider": "gmail", "email_address": "test@example.com"}]
    mock_agent.create_email_account.return_value = {"status": "created", "account_id": "e-new"}
    mock_agent.issue_credential.return_value = {"credential": {"jws": "ey..."}, "message": "Credential issued."}

    return mock_agent

# --- Main Execution ---
def main():
    """Main function to run the agent executor test."""
    print("Initializing mocked CirtusAgent...")
    cirtus_agent = get_mocked_cirtus_agent()

    print("Creating AgentExecutor...")
    # The executor is created with the mocked agent and your DeepSeek key
    executor = create_agent_executor(cirtus_agent, DEEPSEEK_API_KEY)

    # --- Test Prompts ---
    prompts = [
        "What is my master agent?",
        "List my assets for me.",
        "I need a new email account.",
        "Provision a new wallet on the solana chain.",
        "Send the command: check system status",
    ]

    for i, prompt in enumerate(prompts):
        print(f"\n--- Running Test Prompt #{i+1} ---")
        print(f"Prompt: {prompt}")
        try:
            # Invoke the agent with the prompt
            result = executor.invoke({"input": prompt})
            print("\nFinal Answer:")
            print(result.get("output"))
        except Exception as e:
            print(f"An error occurred: {e}")
            # This can happen if the OpenAI key is invalid or the LLM fails

if __name__ == "__main__":
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "YOUR_DEEPSEEK_API_KEY_HERE":
        print("Error: DeepSeek API key is not set.")
        print("Please set the DEEPSEEK_API_KEY environment variable or edit the script.")
    else:
        main()
