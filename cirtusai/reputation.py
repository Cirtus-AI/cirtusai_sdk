from typing import Dict, Any
from requests import Session

class ReputationClient:
    def __init__(self, session: Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def issue_sbt(self, to_address: str, token_uri: str) -> Dict[str, Any]:
        """Issue a new soulbound token."""
        url = f"{self.base_url}/reputation/issue-sbt"
        payload = {"to_address": to_address, "token_uri": token_uri}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_sbt_owner(self, token_id: int) -> str:
        """Get the owner of a soulbound token."""
        url = f"{self.base_url}/reputation/sbt-owner/{token_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
