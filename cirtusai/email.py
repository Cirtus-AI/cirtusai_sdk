import requests
from typing import List, Dict, Any, Type
from langchain_core.tools import BaseTool
from langchain_deepseek import ChatDeepSeek
import pandas as pd
from pydantic import BaseModel, Field
import sys

class EmailClient:
    """
    Client for CirtusAI email services.
    """
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def read_inbox(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Reads the email inbox for a given agent.
        NOTE: This calls the dummy endpoint for demo purposes.
        """
        url = f"{self.base_url}/service/email/inbox"
        headers = {"X-Child-Agent-ID": agent_id}
        resp = self.session.get(url, headers=headers)
        resp.raise_for_status()
        return [resp.json()]


    def send_email(self, agent_id: str, recipient: str, subject: str, body: str) -> Dict[str, Any]:
        """
        Sends an email from a given agent.
        """
        url = f"{self.base_url}/service/email/send"
        headers = {"X-Child-Agent-ID": agent_id}
        payload = {
            "recipient": recipient,
            "subject": subject,
            "body": body
        }
        resp = self.session.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()

class EmailSummarizerTool(BaseTool):
    """Tool to connect to Cirtus, read, and summarize emails."""
    name: str = "read_and_summarize_emails"
    description: str = "Connects to the Cirtus platform to read and summarize emails."
    llm: ChatDeepSeek
    client: Any
    agent_id: str
    username: str
    password: str

    def _run(self) -> str:
        """Execute the tool."""
        print("--- Authenticating with CirtusAI ---")
        sys.stdout.flush()
        try:
            token_response = self.client.auth.login(self.username, self.password)
            self.client.set_token(token_response.access_token)
            print("Authentication successful.")
            sys.stdout.flush()
        except Exception as e:
            return f"Authentication failed: {e}"

        print(f"--- Verifying Permissions for Agent: {self.agent_id} ---")
        sys.stdout.flush()
        try:
            agent_details = self.client.agents.get_agent(self.agent_id)
            permissions = agent_details.get("permissions_granted", [])
            print(f"Agent Permissions: {permissions}")
            sys.stdout.flush()
        except Exception as e:
            return f"Error fetching agent permissions: {e}"

        if "email:read" not in permissions:
            return "Permission Denied: This agent is not authorized to read emails."

        print("--- Permission Granted: Reading Inbox ---")
        sys.stdout.flush()
        try:
            messages = self.client.email.read_inbox(self.agent_id)
        except Exception as e:
            return f"Error reading inbox: {e}"

        if not messages:
            return "No unseen emails."

        print(f"--- Found {len(messages)} messages to summarize ---")
        sys.stdout.flush()

        summaries = []
        for message in messages:
            email_content = message.get("text_body", "")
            sender = message.get("from", "Unknown Sender")
            subject = message.get("subject", "No Subject")

            prompt = f"Please summarize the following email content in one sentence: \n\n{email_content}"
            summary = self.llm.invoke(prompt).content
            summaries.append({
                'Sender': sender,
                'Subject': subject,
                'Summary': summary
            })

        print("--- Formatting Summary ---")
        sys.stdout.flush()
        df = pd.DataFrame(summaries)
        return df.to_csv(index=False)

    async def _arun(self) -> str:
        # The async version of the tool is not implemented
        return self._run()

class SendEmailTool(BaseTool):
    """Tool to send an email."""
    name: str = "send_email"
    description: str = "Sends an email to a specified recipient."
    client: Any
    agent_id: str
    username: str
    password: str

    class SendEmailInput(BaseModel):
        recipient: str = Field(description="The email address of the recipient.")
        subject: str = Field(description="The subject of the email.")
        body: str = Field(description="The body of the email.")

    args_schema: Type[BaseModel] = SendEmailInput

    def _run(self, recipient: str, subject: str, body: str) -> str:
        """Execute the tool."""
        print("--- Authenticating with CirtusAI ---")
        sys.stdout.flush()
        try:
            token_response = self.client.auth.login(self.username, self.password)
            self.client.set_token(token_response.access_token)
            print("Authentication successful.")
            sys.stdout.flush()
        except Exception as e:
            return f"Authentication failed: {e}"

        print(f"--- Verifying Permissions for Agent: {self.agent_id} ---")
        sys.stdout.flush()
        try:
            agent_details = self.client.agents.get_agent(self.agent_id)
            permissions = agent_details.get("permissions_granted", [])
            print(f"Agent Permissions: {permissions}")
            sys.stdout.flush()
        except Exception as e:
            return f"Error fetching agent permissions: {e}"

        if "email:send" not in permissions:
            return "Permission Denied: This agent is not authorized to send emails."

        print("--- Permission Granted: Sending Email ---")
        sys.stdout.flush()
        try:
            self.client.email.send_email(self.agent_id, recipient, subject, body)
            return "Email sent successfully."
        except Exception as e:
            return f"Error sending email: {e}"

    async def _arun(self, recipient: str, subject: str, body: str) -> str:
        # The async version of the tool is not implemented
        return self._run(recipient, subject, body)

class GetEmailAccountTool(BaseTool):
    """Tool to get email account information."""
    name: str = "get_email_account"
    description: str = "Gets email account information from the wallet."
    client: Any
    username: str
    password: str

    def _run(self) -> str:
        """Execute the tool."""
        try:
            token_response = self.client.auth.login(self.username, self.password)
            self.client.set_token(token_response.access_token)
        except Exception as e:
            return f"Authentication failed: {e}"

        try:
            accounts = self.client.wallets.list_email_accounts()
            return f"Email accounts: {accounts}"
        except Exception as e:
            return f"Error getting email account(s): {e}"

class UpdateEmailAccountTool(BaseTool):
    """Tool to update an email account."""
    name: str = "update_email_account"
    description: str = "Updates an email account in the wallet."
    client: Any
    username: str
    password: str

    class UpdateEmailAccountInput(BaseModel):
        account_id: str = Field(description="The ID of the email account to update.")
        provider: str = Field(description="The email provider (e.g., 'imap').")
        email_address: str = Field(description="The email address.")
        config: Dict[str, Any] = Field(description="The email account configuration.")

    args_schema: Type[BaseModel] = UpdateEmailAccountInput

    def _run(self, account_id: str, provider: str, email_address: str, config: Dict[str, Any]) -> str:
        """Execute the tool."""
        try:
            token_response = self.client.auth.login(self.username, self.password)
            self.client.set_token(token_response.access_token)
        except Exception as e:
            return f"Authentication failed: {e}"

        try:
            self.client.wallets.update_email_account(account_id, provider, email_address, config)
            return "Email account updated successfully."
        except Exception as e:
            return f"Error updating email account: {e}"

