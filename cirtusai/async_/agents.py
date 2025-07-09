import httpx
from typing import Any, Dict, List

class AsyncAgentsClient:
    """
    Async client for agent management: master and child agents.
    """
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self.client = client
        self.base_url = base_url.rstrip("/")

    async def list_agents(self) -> List[Dict[str, Any]]:
        response = await self.client.get("/agents")
        response.raise_for_status()
        return response.json()

    async def get_agent(self, agent_id: str) -> Dict[str, Any]:
        response = await self.client.get(f"/agents/{agent_id}")
        response.raise_for_status()
        return response.json()

    async def create_child_agent(self, parent_id: str, name: str) -> Dict[str, Any]:
        path = "/agents/children"
        payload = {"parent_id": parent_id, "name": name}
        response = await self.client.post(path, json=payload)
        response.raise_for_status()
        return response.json()

    async def delete_agent(self, agent_id: str) -> None:
        response = await self.client.delete(f"/agents/{agent_id}")
        response.raise_for_status()

    async def get_children(self) -> List[Dict[str, Any]]:
        """List all child agents linked to the master agent asynchronously."""
        response = await self.client.get("/agents/children")
        response.raise_for_status()
        return response.json()

    async def update_child_permissions(self, child_id: str, permissions: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.put(f"/agents/children/{child_id}/permissions", json={"permissions": permissions})
        response.raise_for_status()
        return response.json()

    async def unlink_child_agent(self, child_id: str) -> None:
        response = await self.client.delete(f"/agents/children/{child_id}")
        response.raise_for_status()

    async def provision_email(self, agent_id: str) -> Dict[str, Any]:
        response = await self.client.post(f"/agents/children/{agent_id}/assets/provision/email")
        response.raise_for_status()
        return response.json()

    async def provision_wallet(self, agent_id: str, chain: str = "ethereum") -> Dict[str, Any]:
        response = await self.client.post(f"/agents/children/{agent_id}/assets/provision/wallet", params={"chain": chain})
        response.raise_for_status()
        return response.json()
