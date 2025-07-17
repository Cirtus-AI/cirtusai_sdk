
import requests
from typing import List, Dict, Any

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
