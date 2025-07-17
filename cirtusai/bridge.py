from typing import Dict, Any
from requests import Session

class BridgeClient:
    def __init__(self, session: Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def get_quote(self, from_chain: str, to_chain: str, from_token: str, to_token: str, amount: int) -> Dict[str, Any]:
        """Get a quote for a cross-chain bridge transfer."""
        url = f"{self.base_url}/wallets/bridge/quote"
        payload = {
            "from_chain": from_chain,
            "to_chain": to_chain,
            "from_token": from_token,
            "to_token": to_token,
            "amount": amount,
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def bridge_transfer(self, provider: str, from_chain: str, to_chain: str, from_token: str, to_token: str, amount: int, recipient_address: str) -> Dict[str, Any]:
        """Execute a cross-chain bridge transfer."""
        url = f"{self.base_url}/wallets/bridge/transfer"
        payload = {
            "provider": provider,
            "from_chain": from_chain,
            "to_chain": to_chain,
            "from_token": from_token,
            "to_token": to_token,
            "amount": amount,
            "recipient_address": recipient_address,
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

class AssetsClient:
    def __init__(self, session: Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def get_multi_chain_asset_view(self) -> Dict[str, Any]:
        """Retrieve a consolidated view of all assets across multiple chains."""
        url = f"{self.base_url}/wallets/assets/view"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def refresh_multi_chain_asset_view(self) -> Dict[str, Any]:
        """Trigger a refresh of the multi-chain asset view."""
        url = f"{self.base_url}/wallets/assets/refresh"
        response = self.session.post(url)
        response.raise_for_status()
        return response.json()
