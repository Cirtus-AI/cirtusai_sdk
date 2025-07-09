import requests
from typing import Dict, Any

class IdentityClient:
    """
    Client for DID and verifiable credential operations.
    """
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def get_did(self, agent_id: str) -> Dict[str, Any]:
        """Retrieve a DID record for the given agent DID or ID."""
        url = f"{self.base_url}/identity/dids/{agent_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def issue_credential(self, subject_id: str, types: list, claim: Dict[str, Any]) -> Dict[str, Any]:
        """Issue a verifiable credential."""
        url = f"{self.base_url}/identity/credentials/issue"
        payload = {"subject_id": subject_id, "type": types, "claim": claim}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def verify_credential(self, jwt_token: str) -> Dict[str, Any]:
        """Verify a verifiable credential token."""
        url = f"{self.base_url}/identity/credentials/verify"
        resp = self.session.post(url, json={"credential": jwt_token})
        resp.raise_for_status()
        return resp.json()
