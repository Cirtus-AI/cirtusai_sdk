import requests
from typing import List, Dict, Any

class WalletsClient:
    """
    Client for wallet asset and email account management.
    """
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def list_assets(self) -> Dict[str, Any]:
        """List all wallet assets."""
        url = f"{self.base_url}/wallets"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def list_email_accounts(self) -> List[Dict[str, Any]]:
        """List all linked email accounts."""
        url = f"{self.base_url}/wallets/email_accounts"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def create_email_account(self, provider: str, email_address: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new email account in the wallet."""
        url = f"{self.base_url}/wallets/email_accounts"
        payload = {"provider": provider, "email_address": email_address, "config": config}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def refresh_email_token(self, account_id: str) -> Dict[str, Any]:
        """Refresh OAuth token for an email account."""
        url = f"{self.base_url}/wallets/email_accounts/{account_id}/refresh"
        resp = self.session.post(url)
        resp.raise_for_status()
        return resp.json()

    def add_asset(self, asset_key: str, asset_value: str) -> None:
        """Add a single asset to the master agent's vault."""
        url = f"{self.base_url}/wallets/assets"
        payload = {"asset_key": asset_key, "asset_value": asset_value}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()

    def bulk_add_assets(self, assets: Dict[str, str]) -> None:
        """Bulk add assets to the master agent's vault."""
        url = f"{self.base_url}/wallets/assets/bulk"
        payload = {"assets": assets}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()

    def add_crypto(self, chain: str = "ethereum") -> Dict[str, Any]:
        """Add a new crypto wallet asset to the master agent."""
        url = f"{self.base_url}/wallets/crypto"
        resp = self.session.post(url, params={"chain": chain})
        resp.raise_for_status()
        return resp.json()

    def get_email_account(self, account_id: str) -> Dict[str, Any]:
        """Retrieve a single email account detail."""
        url = f"{self.base_url}/wallets/email_accounts/{account_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def update_email_account(self, account_id: str, provider: str, email_address: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing email account's configuration."""
        url = f"{self.base_url}/wallets/email_accounts/{account_id}"
        payload = {"provider": provider, "email_address": email_address, "config": config}
        resp = self.session.put(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def delete_email_account(self, account_id: str) -> None:
        """Delete an email account from the wallet."""
        url = f"{self.base_url}/wallets/email_accounts/{account_id}"
        resp = self.session.delete(url)
        resp.raise_for_status()
