import os
import pandas as pd
from langchain_core.tools import BaseTool
from langchain_deepseek import ChatDeepSeek
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from cirtusai.client import CirtusAIClient
from cirtusai.email import EmailSummarizerTool, SendEmailTool, GetEmailAccountTool, UpdateEmailAccountTool
from typing import Type
from pydantic import BaseModel, Field
import sys

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
CIRTUS_AGENT_ID = os.getenv("CIRTUS_AGENT_ID")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# --- CirtusAI Client Initialization ---
try:
    client = CirtusAIClient(base_url=CIRTUS_API_URL)
except Exception as e:
    sys.stderr.write(f"Error initializing CirtusAIClient: {e}\n")
    sys.exit(1)

# --- Main Execution ---

def main():
    """Initializes and runs the email summarizer agent."""
    if not all([CIRTUS_USERNAME, CIRTUS_PASSWORD, CIRTUS_AGENT_ID, DEEPSEEK_API_KEY]):
        sys.stderr.write("Error: Missing required environment variables in .env file.\n")
        sys.exit(1)

    print("--- Initializing Email Summarizer Agent ---")
    sys.stdout.flush()

    try:
        llm = ChatDeepSeek(model="deepseek-chat", api_key=DEEPSEEK_API_KEY, temperature=0)
    except Exception as e:
        sys.stderr.write(f"Error initializing ChatDeepSeek: {e}\n")
        sys.exit(1)
    
    # Instantiate the class-based tool
    summarize_tool = EmailSummarizerTool(
        llm=llm, 
        client=client, 
        agent_id=CIRTUS_AGENT_ID, 
        username=CIRTUS_USERNAME, 
        password=CIRTUS_PASSWORD
    )
    send_email_tool = SendEmailTool(
        client=client, 
        agent_id=CIRTUS_AGENT_ID, 
        username=CIRTUS_USERNAME, 
        password=CIRTUS_PASSWORD
    )
    get_email_account_tool = GetEmailAccountTool(
        client=client,
        username=CIRTUS_USERNAME,
        password=CIRTUS_PASSWORD
    )
    update_email_account_tool = UpdateEmailAccountTool(
        client=client,
        username=CIRTUS_USERNAME,
        password=CIRTUS_PASSWORD
    )

    tools = [summarize_tool, send_email_tool, get_email_account_tool, update_email_account_tool]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that can summarize and send emails. You can read emails by asking me to 'read emails' or 'summarize my inbox'. You can send emails by asking me to 'send an email to [recipient] with subject [subject] and body [body]'. You can also get and update email account information."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_openai_tools_agent(llm, tools, prompt)

    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    print("--- Starting Interactive Agent ---")
    sys.stdout.flush()
    print("Type 'exit' or 'quit' to end the session.")
    sys.stdout.flush()

    while True:
        user_input = input("\nYour command: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting agent session.")
            sys.stdout.flush()
            break
        
        try:
            result = executor.invoke({"input": user_input})
            print("\nAgent Response:")
            sys.stdout.flush()
            print(result['output'])
            sys.stdout.flush()
        except Exception as e:
            print(f"An error occurred during agent execution: {e}")
            sys.stdout.flush()

    print("Script finished.")
    sys.stdout.flush()

if __name__ == "__main__":
    main()