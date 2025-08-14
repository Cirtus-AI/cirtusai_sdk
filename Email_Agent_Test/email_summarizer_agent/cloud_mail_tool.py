
import requests
import os
import sys
import pandas as pd
from langchain_core.tools import BaseTool
from pydantic import Field, BaseModel
from typing import Type, List, Any, Dict
from langchain_deepseek import ChatDeepSeek

class CloudMailClient:
    def __init__(self, cloud_mail_url, cloud_mail_email, cloud_mail_password):
        self.base_url = cloud_mail_url
        if not self.base_url.startswith("http"):
            self.base_url = "https://" + self.base_url
        self.email = cloud_mail_email
        self.password = cloud_mail_password
        self.token = None

    def login(self):
        login_url = f"{self.base_url}/api/login"
        payload = {"email": self.email, "password": self.password}
        response = requests.post(login_url, json=payload)
        response.raise_for_status()
        self.token = response.json()["data"]["token"]

    def get_headers(self):
        if not self.token:
            self.login()
        return {"Authorization": self.token}

    def get_user_info(self):
        user_info_url = f"{self.base_url}/api/my/loginUserInfo"
        response = requests.get(user_info_url, headers=self.get_headers())
        response.raise_for_status()
        return response.json()["data"]

    def list_emails(self, account_id):
        list_url = f"{self.base_url}/api/email/list?accountId={account_id}&type=0&size=10&timeSort=0"
        response = requests.get(list_url, headers=self.get_headers())
        response.raise_for_status()
        return response.json()["data"]["list"]

    def send_email(self, account_id, name, recipient, subject, body):
        payload = {
            "accountId": account_id,
            "name": name,
            "receiveEmail": [recipient],
            "subject": subject,
            "content": body,
            "text": body,
            "attachments": []
        }
        send_url = f"{self.base_url}/api/email/send"
        response = requests.post(send_url, headers=self.get_headers(), json=payload)
        response.raise_for_status()

class SendEmailInput(BaseModel):
    recipient: str = Field(description="The recipient's email address.")
    subject: str = Field(description="The subject of the email.")
    body: str = Field(description="The body of the email.")

class CloudMailSendEmailTool(BaseTool):
    name: str = "send_email"
    description: str = "Sends an email to a recipient with a subject and body."
    args_schema: Type[BaseModel] = SendEmailInput
    client: Any
    agent_id: str
    username: str
    password: str
    cloud_mail_client: CloudMailClient

    def _run(self, recipient: str, subject: str, body: str) -> str:
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
            master_agent = self.client.agents.list_agents()
            if not master_agent:
                return "Error: Could not find master agent."
            
            child_agent = next((agent for agent in master_agent.get('state', {}).get('linked_children', []) if agent.get('child_agent_id') == self.agent_id), None)

            if not child_agent:
                return f"Error: Child agent '{self.agent_id}' not found."

            permissions = child_agent.get("permissions_granted", [])
            print(f"Agent Permissions: {permissions}")
            sys.stdout.flush()
        except Exception as e:
            return f"Error fetching agent permissions: {e}"

        if "send_email" not in permissions:
            return "Permission Denied: This agent is not authorized to send emails."

        print("--- Permission Granted: Sending Email ---")
        sys.stdout.flush()
        try:
            user_info = self.cloud_mail_client.get_user_info()
            account_id = user_info["accountId"]
            sender_name = user_info["name"]
            self.cloud_mail_client.send_email(account_id, sender_name, recipient, subject, body)
            return "Email sent successfully."
        except Exception as e:
            return f"Error sending email: {e}"

class CloudMailReadAndSummarizeEmailTool(BaseTool):
    name: str = "read_and_summarize_emails"
    description: str = "Connects to the Cirtus platform to read and summarize emails."
    llm: ChatDeepSeek
    client: Any
    agent_id: str
    username: str
    password: str
    cloud_mail_client: CloudMailClient

    def _run(self) -> str:
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
            master_agent = self.client.agents.list_agents()
            if not master_agent:
                return "Error: Could not find master agent."
            
            child_agent = next((agent for agent in master_agent.get('state', {}).get('linked_children', []) if agent.get('child_agent_id') == self.agent_id), None)

            if not child_agent:
                return f"Error: Child agent '{self.agent_id}' not found."

            permissions = child_agent.get("permissions_granted", [])
            print(f"Agent Permissions: {permissions}")
            sys.stdout.flush()
        except Exception as e:
            return f"Error fetching agent permissions: {e}"

        if "read_email" not in permissions:
            return "Permission Denied: This agent is not authorized to read emails."

        print("--- Permission Granted: Reading Inbox ---")
        sys.stdout.flush()
        try:
            user_info = self.cloud_mail_client.get_user_info()
            account_id = user_info["accountId"]
            messages = self.cloud_mail_client.list_emails(account_id)
        except Exception as e:
            return f"Error reading inbox: {e}"

        if not messages:
            return "No unseen emails."

        print(f"--- Found {len(messages)} messages to summarize ---")
        sys.stdout.flush()

        summaries = []
        for message in messages:
            email_content = message.get("text", "")
            sender = message.get("sendEmail", "Unknown Sender")
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

class CloudMailGetAccountInfoTool(BaseTool):
    name: str = "get_email_account_information"
    description: str = "Gets information about the user's email account."
    client: Any
    username: str
    password: str
    cloud_mail_client: CloudMailClient

    def _run(self) -> dict:
        print("--- Authenticating with CirtusAI ---")
        sys.stdout.flush()
        try:
            token_response = self.client.auth.login(self.username, self.password)
            self.client.set_token(token_response.access_token)
            print("Authentication successful.")
            sys.stdout.flush()
        except Exception as e:
            return f"Authentication failed: {e}"
        
        return self.cloud_mail_client.get_user_info()
