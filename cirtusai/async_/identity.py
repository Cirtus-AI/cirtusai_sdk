import httpx
from typing import Dict, Any, List

class AsyncIdentityClient:
    """
    Async client for DID and verifiable credential operations.
    """
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self.client = client
        self.base_url = base_url.rstrip("/")

    async def get_did(self, agent_id: str) -> Dict[str, Any]:
        """Retrieve a DID record for the given agent DID or ID."""
        url = f"{self.base_url}/identity/dids/{agent_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def issue_credential(self, subject_id: str, types: List[str], claim: Dict[str, Any]) -> Dict[str, Any]:
        """Issue a verifiable credential."""
        url = f"{self.base_url}/identity/credentials/issue"
        payload = {"subject_id": subject_id, "type": types, "claim": claim}
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    async def verify_credential(self, jwt_token: str) -> Dict[str, Any]:
        """Verify a verifiable credential token."""
        url = f"{self.base_url}/identity/credentials/verify"
        response = await self.client.post(url, json={"credential": jwt_token})
        response.raise_for_status()
        return response.json()
