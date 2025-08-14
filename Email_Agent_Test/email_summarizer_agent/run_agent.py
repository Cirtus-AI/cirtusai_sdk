import os
from langchain_deepseek import ChatDeepSeek
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from cirtusai.client import CirtusAIClient
from cloud_mail_tool import CloudMailClient, CloudMailSendEmailTool, CloudMailReadAndSummarizeEmailTool, CloudMailGetAccountInfoTool
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
CLOUD_MAIL_URL = os.getenv("CLOUD_MAIL_URL")
CLOUD_MAIL_EMAIL = os.getenv("CLOUD_MAIL_EMAIL")
CLOUD_MAIL_PASSWORD = os.getenv("CLOUD_MAIL_PASSWORD")

# --- CirtusAI Client Initialization ---
try:
    client = CirtusAIClient(base_url=CIRTUS_API_URL)
except Exception as e:
    sys.stderr.write(f"Error initializing CirtusAIClient: {e}\n")
    sys.exit(1)

# --- Main Execution ---

def main():
    """Initializes and runs the email summarizer agent."""
    if not all([CIRTUS_USERNAME, CIRTUS_PASSWORD, CIRTUS_AGENT_ID, DEEPSEEK_API_KEY, CLOUD_MAIL_URL, CLOUD_MAIL_EMAIL, CLOUD_MAIL_PASSWORD]):
        sys.stderr.write("Error: Missing required environment variables in .env file.\n")
        sys.exit(1)

    print("--- Initializing Email Summarizer Agent ---")
    sys.stdout.flush()

    try:
        llm = ChatDeepSeek(model="deepseek-chat", api_key=DEEPSEEK_API_KEY, temperature=0)
    except Exception as e:
        sys.stderr.write(f"Error initializing ChatDeepSeek: {e}\n")
        sys.exit(1)
    
    # Instantiate the cloud-mail client
    cloud_mail_client = CloudMailClient(
        cloud_mail_url=CLOUD_MAIL_URL,
        cloud_mail_email=CLOUD_MAIL_EMAIL,
        cloud_mail_password=CLOUD_MAIL_PASSWORD
    )

    # Instantiate the class-based tools
    send_email_tool = CloudMailSendEmailTool(
        client=client,
        agent_id=CIRTUS_AGENT_ID,
        username=CIRTUS_USERNAME,
        password=CIRTUS_PASSWORD,
        cloud_mail_client=cloud_mail_client
    )
    read_summarize_tool = CloudMailReadAndSummarizeEmailTool(
        llm=llm,
        client=client,
        agent_id=CIRTUS_AGENT_ID,
        username=CIRTUS_USERNAME,
        password=CIRTUS_PASSWORD,
        cloud_mail_client=cloud_mail_client
    )
    get_email_account_tool = CloudMailGetAccountInfoTool(
        client=client,
        username=CIRTUS_USERNAME,
        password=CIRTUS_PASSWORD,
        cloud_mail_client=cloud_mail_client
    )

    tools = [send_email_tool, read_summarize_tool, get_email_account_tool]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that can read, summarize and send emails using the cloud-mail server. You can read and summarize emails by asking me to 'read and summarize emails'. You can send emails by asking me to 'send an email to [recipient] with subject [subject] and body [body]'. You can also get your email account information."),
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
