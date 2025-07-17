from typing import List, Dict, Any
from requests import Session

class GovernanceClient:
    def __init__(self, session: Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def create_proposal(self, targets: List[str], values: List[int], calldatas: List[str], description: str) -> Dict[str, Any]:
        """Create a new governance proposal."""
        url = f"{self.base_url}/governance/proposals"
        payload = {
            "targets": targets,
            "values": values,
            "calldatas": calldatas,
            "description": description,
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def cast_vote(self, proposal_id: int, support: int) -> Dict[str, Any]:
        """Cast a vote on a governance proposal."""
        url = f"{self.base_url}/governance/vote"
        payload = {"proposal_id": proposal_id, "support": support}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_proposal_state(self, proposal_id: int) -> Dict[str, Any]:
        """Get the state of a governance proposal."""
        url = f"{self.base_url}/governance/proposals/{proposal_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
