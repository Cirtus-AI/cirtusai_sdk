import httpx
from typing import Optional
from .auth import AsyncAuthClient
from .agents import AsyncAgentsClient
from .wallets import AsyncWalletsClient
from .identity import AsyncIdentityClient

class AsyncCirtusAIClient:
    """
    Asynchronous client for CirtusAI: wraps sub-clients for auth, agents, wallets, and identity.
    """
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(base_url=self.base_url, headers={
            **({"Authorization": f"Bearer {token}"} if token else {}),
            "Content-Type": "application/json"
        })
        self.auth = AsyncAuthClient(self.client, self.base_url)
        self.agents = AsyncAgentsClient(self.client, self.base_url)
        self.wallets = AsyncWalletsClient(self.client, self.base_url)
        self.identity = AsyncIdentityClient(self.client, self.base_url)

    async def set_token(self, token: str):
        """Update Authorization header."""
        self.client.headers["Authorization"] = f"Bearer {token}"

    async def close(self):
        """Close the underlying HTTP session."""
        await self.client.aclose()
