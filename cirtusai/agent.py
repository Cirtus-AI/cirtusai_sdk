import requests

class CirtusAgent:
    """
    Python SDK client for CirtusAI backend. Wraps the REST API for agent and wallet management.
    """
    def __init__(self, agent_id: str, token: str, base_url: str = "http://localhost:8000"):
        """
        :param agent_id: The child agent's ID or master agent DID
        :param token: JWT access token (Bearer)
        :param base_url: Base URL of the CirtusAI API
        """
        self.agent_id = agent_id
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}", "Content-Type": "application/json"})

    def list_master_agent(self) -> dict:
        """Fetch the master agent record for the current user."""
        url = f"{self.base_url}/agents"
        resp = self.session.request("GET", url)
        resp.raise_for_status()
        return resp.json()

    def list_assets(self) -> dict:
        """Get all wallet assets for the master agent."""
        url = f"{self.base_url}/wallets"
        resp = self.session.request("GET", url)
        resp.raise_for_status()
        return resp.json()

    def provision_email(self) -> dict:
        """Provision a new email asset for this child agent."""
        url = f"{self.base_url}/agents/children/{self.agent_id}/assets/provision/email"
        resp = self.session.request("POST", url)
        resp.raise_for_status()
        return resp.json()

    def provision_wallet(self, chain: str = "ethereum") -> dict:
        """Provision a new crypto wallet asset for this child agent."""
        url = f"{self.base_url}/agents/children/{self.agent_id}/assets/provision/wallet"
        resp = self.session.request("POST", url, params={"chain": chain})
        resp.raise_for_status()
        return resp.json()

    def command(self, text: str) -> dict:
        """Send a command to the message bus for this agent."""
        url = f"{self.base_url}/command"
        resp = self.session.request("POST", url, json={"text": text})
        resp.raise_for_status()
        return resp.json()

    def list_email_accounts(self) -> list:
        """List all email accounts linked to the user wallet."""
        url = f"{self.base_url}/wallets/email_accounts"
        resp = self.session.request("GET", url)
        resp.raise_for_status()
        return resp.json()

    def create_email_account(self, provider: str, email_address: str, config: dict) -> dict:
        """Create a new email account in the wallet."""
        url = f"{self.base_url}/wallets/email_accounts"
        resp = self.session.request("POST", url, json={"provider": provider, "email_address": email_address, "config": config})
        resp.raise_for_status()
        return resp.json()

    def issue_credential(self, subject_id: str, types: list, claim: dict) -> dict:
        """Issue a verifiable credential from the master agent DID."""
        url = f"{self.base_url}/identity/credentials/issue"
        resp = self.session.request("POST", url, json={"subject_id": subject_id, "type": types, "claim": claim})
        resp.raise_for_status()
        return resp.json()
