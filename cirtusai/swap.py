import requests
from typing import Dict, Any

class SwapClient:
    """
    Client for token swap operations: quote, execute, cancel.
    """
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def get_quote(self, from_chain: str, to_chain: str, from_token: str, to_token: str, amount: float) -> Dict[str, Any]:
        """Get a swap quote for a token pair."""
        url = f"{self.base_url}/swap/quote"
        params = {
            "from_chain": from_chain,
            "to_chain": to_chain,
            "from_token": from_token,
            "to_token": to_token,
            "amount": amount
        }
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def execute_swap(self, swap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a token swap based on quote or parameters."""
        url = f"{self.base_url}/swap/execute"
        resp = self.session.post(url, json=swap_data)
        resp.raise_for_status()
        return resp.json()

    def cancel_swap(self, swap_id: str) -> None:
        """Cancel a pending swap by ID."""
        url = f"{self.base_url}/swap/cancel/{swap_id}"
        resp = self.session.post(url)
        resp.raise_for_status()
