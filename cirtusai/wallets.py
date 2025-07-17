import requests
from typing import List, Dict, Any
from decimal import Decimal

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
        url = f"{self.base_url}/wallets/email_accounts/"
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

    def send_transaction(self, chain: str, to: str, signed_tx: str) -> str:
        """Send a raw transaction on a supported chain."""
        url = f"{self.base_url}/wallets/send"
        payload = {"chain": chain, "to": to, "signed_tx": signed_tx}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def get_balance(self, chain: str, address: str) -> Decimal:
        """Get balance of an address on a supported chain."""
        url = f"{self.base_url}/wallets/balance/{chain}/{address}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return Decimal(resp.json().get("balance"))

    # Gas Sponsorship
    def sponsor_gas(self, token_address: str, amount: Decimal) -> str:
        """Deposit ERC-20 tokens into your gas sponsorship pool."""
        url = f"{self.base_url}/wallets/gas/sponsor"
        payload = {"token_address": token_address, "amount": str(amount)}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def get_gas_sponsorship_balance(self) -> Decimal:
        """Get your current gas sponsorship token balance."""
        url = f"{self.base_url}/wallets/gas/balance"
        resp = self.session.get(url)
        resp.raise_for_status()
        return Decimal(resp.json())

    # Fiat On/Off-Ramp
    def create_onramp_session(self, currency: str, amount: float) -> Dict[str, Any]:
        """Initiate a fiat on-ramp session and retrieve widget URL or session token."""
        url = f"{self.base_url}/wallets/fiat/onramp"
        resp = self.session.post(url, json={"currency": currency, "amount": amount})
        resp.raise_for_status()
        return resp.json()

    def get_onramp_status(self, session_id: str) -> Dict[str, Any]:
        """Retrieve status of a fiat on-ramp session."""
        url = f"{self.base_url}/wallets/fiat/status/{session_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    # RWA Registry
    def register_rwa_asset(self, token_address: str, token_id: str, metadata_uri: str = None) -> Dict[str, Any]:
        """Register a real-world asset token into your vault."""
        url = f"{self.base_url}/wallets/rwa"
        payload = {"token_address": token_address, "token_id": token_id, "metadata_uri": metadata_uri}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def list_rwa_assets(self) -> List[Dict[str, Any]]:
        """List all registered RWA assets in your vault."""
        url = f"{self.base_url}/wallets/rwa"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def transfer_rwa_asset(self, asset_id: str, to_address: str) -> str:
        """Transfer a registered RWA asset to another address."""
        url = f"{self.base_url}/wallets/rwa/{asset_id}/transfer"
        resp = self.session.post(url, json={"to_address": to_address})
        resp.raise_for_status()
        return resp.json()

    # Yield Vault Automation
    def create_yield_strategy(self, asset_key: str, protocol: str, min_apr: Decimal) -> Dict[str, Any]:
        """Create a new automated yield strategy."""
        url = f"{self.base_url}/wallets/strategies"
        payload = {"asset_key": asset_key, "protocol": protocol, "min_apr": str(min_apr)}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def list_yield_strategies(self) -> List[Dict[str, Any]]:
        """List all yield strategies."""
        url = f"{self.base_url}/wallets/strategies"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def run_yield_strategy(self, strategy_id: str) -> Dict[str, Any]:
        """Execute or rebalance a yield strategy on-demand."""
        url = f"{self.base_url}/wallets/strategies/{strategy_id}/run"
        resp = self.session.post(url)
        resp.raise_for_status()
        return resp.json()

    # On-chain event subscriptions
    def subscribe_event(self, chain: str, filter_criteria: Dict[str, Any], callback_url: str) -> str:
        """Subscribe to on-chain events and receive a subscription ID."""
        url = f"{self.base_url}/wallets/events"
        payload = {"chain": chain, "filter_criteria": filter_criteria, "callback_url": callback_url}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def list_event_subscriptions(self) -> List[Dict[str, Any]]:
        """List all on-chain event subscriptions."""
        url = f"{self.base_url}/wallets/events"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def unsubscribe_event(self, subscription_id: str) -> None:
        """Remove an on-chain event subscription."""
        url = f"{self.base_url}/wallets/events/{subscription_id}"
        resp = self.session.delete(url)
        resp.raise_for_status()

    # Agent smart contract wallet management (Phase 1)
    def deploy_agent_wallet(self) -> Dict[str, Any]:
        """Deploy a new CirtusWallet contract for the authenticated user."""
        url = f"{self.base_url}/agents/wallets/"
        resp = self.session.post(url)
        resp.raise_for_status()
        return resp.json()

    def list_agent_wallets(self) -> List[Dict[str, Any]]:
        """Retrieve all deployed CirtusWallet contracts for the user."""
        url = f"{self.base_url}/agents/wallets/"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_agent_wallet(self, address: str) -> Dict[str, Any]:
        """Get details of a specific CirtusWallet by address."""
        url = f"{self.base_url}/agents/wallets/{address}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def set_spending_limit(self, address: str, token: str, amount: int, period: int) -> str:
        """Set the on-chain spending limit for a token."""
        url = f"{self.base_url}/agents/wallets/{address}/spending_limit"
        payload = {"token": token, "amount": amount, "period": period}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def update_whitelist(self, address: str, target: str, allowed: bool) -> str:
        """Add or remove a whitelisted address on-chain."""
        url = f"{self.base_url}/agents/wallets/{address}/whitelist"
        payload = {"target": target, "allowed": allowed}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def set_threshold(self, address: str, new_threshold: int) -> str:
        """Adjust the transaction threshold on-chain."""
        url = f"{self.base_url}/agents/wallets/{address}/threshold"
        payload = {"new_threshold": new_threshold}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def list_wallet_transactions(self, address: str) -> List[Dict[str, Any]]:
        """Fetch the history of on-chain events for a specific wallet."""
        url = f"{self.base_url}/agents/wallets/{address}/transactions"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def create_wallet(self, chain: str) -> Dict[str, Any]:
        response = self.session.post("/wallets/", json={"chain": chain})
        response.raise_for_status()
        return response.json()

    def import_wallet(self, chain: str, private_key: str) -> Dict[str, Any]:
        response = self.session.post("/wallets/import", json={"chain": chain, "private_key": private_key})
        response.raise_for_status()
        return response.json()

    def list_wallets(self) -> List[Dict[str, Any]]:
        response = self.session.get("/wallets/")
        response.raise_for_status()
        return response.json()

    def delete_wallet(self, wallet_id: str) -> None:
        response = self.session.delete(f"/wallets/{wallet_id}")
        response.raise_for_status()

    def get_token_balance(self, wallet_id: str, token_address: str) -> Dict[str, Any]:
        response = self.session.get(f"/wallets/{wallet_id}/tokens/{token_address}/balance")
        response.raise_for_status()
        return response.json()

    def transfer_tokens(self, wallet_id: str, token_address: str, to_address: str, amount: float) -> Dict[str, Any]:
        payload = {"token_address": token_address, "to_address": to_address, "amount": amount}
        response = self.session.post(f"/wallets/{wallet_id}/tokens/transfer", json=payload)
        response.raise_for_status()
        return response.json()

    def approve_tokens(self, wallet_id: str, token_address: str, spender_address: str, amount: float) -> Dict[str, Any]:
        payload = {"token_address": token_address, "spender_address": spender_address, "amount": amount}
        response = self.session.post(f"/wallets/{wallet_id}/tokens/approve", json=payload)
        response.raise_for_status()
        return response.json()

    def send_user_operation(self, user_op: Dict[str, Any], entry_point_address: str) -> Dict[str, Any]:
        payload = {"user_op": user_op, "entry_point_address": entry_point_address}
        response = self.session.post("/wallets/account-ops/send", json=payload)
        response.raise_for_status()
        return response.json()

    def get_user_operation_status(self, user_op_hash: str) -> Dict[str, Any]:
        response = self.session.get(f"/wallets/account-ops/status/{user_op_hash}")
        response.raise_for_status()
        return response.json()
