import os
import sys
from dotenv import load_dotenv
from cirtusai.client import CirtusAIClient

# Load environment variables from .env file
try:
    load_dotenv()
except Exception as e:
    sys.stderr.write(f"Error loading .env file: {e}\n")
    sys.exit(1)

# --- Configuration ---
CIRTUS_API_URL = os.getenv("CIRTUS_API_URL", "http://localhost:8000")
CIRTUS_USERNAME = os.getenv("CIRTUS_USERNAME")
CIRTUS_PASSWORD = os.getenv("CIRTUS_PASSWORD")

# --- CirtusAI Client Initialization ---
try:
    client = CirtusAIClient(base_url=CIRTUS_API_URL)
    token_data = client.auth.login(username=CIRTUS_USERNAME, password=CIRTUS_PASSWORD)
    client.set_token(token_data.access_token)
except Exception as e:
    sys.stderr.write(f"Error initializing CirtusAIClient or logging in: {e}\n")
    sys.exit(1)

def list_child_agents():
    """Lists all child agents for the logged-in user's master agent."""
    print("--- Listing Child Agents ---")
    try:
        child_agents = client.agents.get_children()
        print(child_agents)
        
        if not child_agents:
            print("No child agents found for this master agent.")
            return

        print("Found the following child agents:")
        for agent in child_agents:
            print(f"  - Name: {agent.get('child_agent_id')}, ID: {agent.get('id')}")

    except Exception as e:
        print(f"An error occurred while listing agents: {e}")

if __name__ == "__main__":
    list_child_agents()