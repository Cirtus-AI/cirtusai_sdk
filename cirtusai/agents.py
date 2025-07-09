import requests
from typing import Optional, Dict, Any, List

class AgentsClient:
    """
    Client for agent management: master and child agents.
    """
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def list_agents(self) -> List[Dict[str, Any]]:
        """List all master agents for the logged-in user."""
        url = f"{self.base_url}/agents"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Retrieve a specific agent by DID or ID."""
        url = f"{self.base_url}/agents/{agent_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def create_child_agent(self, parent_id: str, name: str) -> Dict[str, Any]:
        """Create a new child agent under a master agent."""
        url = f"{self.base_url}/agents/children"
        payload = {"parent_id": parent_id, "name": name}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def delete_agent(self, agent_id: str) -> None:
        """Delete an agent by ID."""
        url = f"{self.base_url}/agents/{agent_id}"
        resp = self.session.delete(url)
        resp.raise_for_status()

    def provision_email(self, agent_id: str) -> Dict[str, Any]:
        """Provision an email asset for the specified child agent."""
        url = f"{self.base_url}/agents/children/{agent_id}/assets/provision/email"
        resp = self.session.post(url)
        resp.raise_for_status()
        return resp.json()

    def provision_wallet(self, agent_id: str, chain: str = "ethereum") -> Dict[str, Any]:
        """Provision a crypto wallet asset for the specified child agent."""
        url = f"{self.base_url}/agents/children/{agent_id}/assets/provision/wallet"
        resp = self.session.post(url, params={"chain": chain})
        resp.raise_for_status()
        return resp.json()

    def get_children(self) -> List[Dict[str, Any]]:
        """List all child agents linked to the master agent."""
        url = f"{self.base_url}/agents/children"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def update_child_permissions(self, child_id: str, permissions: Dict[str, Any]) -> Dict[str, Any]:
        """Update permissions for a specific child agent."""
        url = f"{self.base_url}/agents/children/{child_id}/permissions"
        resp = self.session.put(url, json={"permissions": permissions})
        resp.raise_for_status()
        return resp.json()

    def unlink_child_agent(self, child_id: str) -> None:
        """Unlink (delete) a child agent from master agent."""
        url = f"{self.base_url}/agents/children/{child_id}"
        resp = self.session.delete(url)
        resp.raise_for_status()
