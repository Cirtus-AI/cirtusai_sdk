import httpx
from typing import Dict, Any

class AsyncAuthClient:
    """
    Async authentication client for CirtusAI: login and token refresh.
    """
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self.client = client
        self.base_url = base_url.rstrip("/")

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/auth/login"
        response = await self.client.post(url, json={"email": email, "password": password})
        response.raise_for_status()
        return response.json()

    async def refresh(self, refresh_token: str) -> Dict[str, Any]:
        url = f"{self.base_url}/auth/refresh"
        response = await self.client.post(url, json={"refresh_token": refresh_token})
        response.raise_for_status()
        return response.json()
