import httpx
from typing import Any, Dict, List

class AsyncWalletsClient:
    """
    Async client for wallet asset and email account management.
    """
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self.client = client
        self.base_url = base_url.rstrip("/")

    async def list_assets(self) -> Dict[str, Any]:
        """List all wallet assets."""
        url = f"{self.base_url}/wallets"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def list_email_accounts(self) -> List[Dict[str, Any]]:
        """List all linked email accounts."""
        url = f"{self.base_url}/wallets/email_accounts"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def create_email_account(self, provider: str, email_address: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new email account in the wallet."""
        url = f"{self.base_url}/wallets/email_accounts"
        payload = {"provider": provider, "email_address": email_address, "config": config}
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    async def refresh_email_token(self, account_id: str) -> Dict[str, Any]:
        """Refresh OAuth token for an email account."""
        url = f"{self.base_url}/wallets/email_accounts/{account_id}/refresh"
        response = await self.client.post(url)
        response.raise_for_status()
        return response.json()
