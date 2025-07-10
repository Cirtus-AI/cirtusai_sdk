import httpx
from typing import Any, Dict, List
from decimal import Decimal

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

    async def send_transaction(self, chain: str, to: str, signed_tx: str) -> str:
        """Send a raw transaction on a supported chain."""
        url = f"{self.base_url}/wallets/send"
        payload = {"chain": chain, "to": to, "signed_tx": signed_tx}
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    async def get_balance(self, chain: str, address: str) -> Decimal:
        """Get the balance of an address on a supported chain."""
        url = f"{self.base_url}/wallets/balance/{chain}/{address}"
        response = await self.client.get(url)
        response.raise_for_status()
        data = response.json()
        return Decimal(data.get("balance"))

    async def sponsor_gas(self, token_address: str, amount: str) -> str:
        """Deposit ERC-20 tokens into your gas sponsorship pool."""
        url = f"{self.base_url}/wallets/gas/sponsor"
        response = await self.client.post(url, json={"token_address": token_address, "amount": amount})
        response.raise_for_status()
        return response.json()

    async def get_gas_sponsorship_balance(self) -> Decimal:
        """Get your current gas sponsorship token balance."""
        url = f"{self.base_url}/wallets/gas/balance"
        response = await self.client.get(url)
        response.raise_for_status()
        return Decimal(response.json())

    async def create_onramp_session(self, currency: str, amount: float) -> Dict[str, Any]:
        """Initiate a fiat on-ramp session and retrieve widget URL or session token."""
        url = f"{self.base_url}/wallets/fiat/onramp"
        response = await self.client.post(url, json={"currency": currency, "amount": amount})
        response.raise_for_status()
        return response.json()

    async def get_onramp_status(self, session_id: str) -> Dict[str, Any]:
        """Retrieve status of a fiat on-ramp session."""
        url = f"{self.base_url}/wallets/fiat/status/{session_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def register_rwa_asset(self, token_address: str, token_id: str, metadata_uri: str = None) -> Dict[str, Any]:
        """Register a real-world asset token into your vault."""
        url = f"{self.base_url}/wallets/rwa"
        response = await self.client.post(url, json={"token_address": token_address, "token_id": token_id, "metadata_uri": metadata_uri})
        response.raise_for_status()
        return response.json()

    async def list_rwa_assets(self) -> List[Dict[str, Any]]:
        """List all registered RWA assets in your vault."""
        url = f"{self.base_url}/wallets/rwa"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def transfer_rwa_asset(self, asset_id: str, to_address: str) -> str:
        """Transfer a registered RWA asset to another address."""
        url = f"{self.base_url}/wallets/rwa/{asset_id}/transfer"
        response = await self.client.post(url, json={"to_address": to_address})
        response.raise_for_status()
        return response.json()

    async def create_yield_strategy(self, asset_key: str, protocol: str, min_apr: str) -> Dict[str, Any]:
        """Create a new automated yield strategy."""
        url = f"{self.base_url}/wallets/strategies"
        response = await self.client.post(url, json={"asset_key": asset_key, "protocol": protocol, "min_apr": min_apr})
        response.raise_for_status()
        return response.json()

    async def list_yield_strategies(self) -> List[Dict[str, Any]]:
        """List all yield strategies."""
        url = f"{self.base_url}/wallets/strategies"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def run_yield_strategy(self, strategy_id: str) -> Dict[str, Any]:
        """Execute or rebalance a yield strategy on-demand."""
        url = f"{self.base_url}/wallets/strategies/{strategy_id}/run"
        response = await self.client.post(url)
        response.raise_for_status()
        return response.json()

    # On-chain event subscriptions
    async def subscribe_event(self, chain: str, filter_criteria: Dict[str, Any], callback_url: str) -> str:
        """Subscribe to on-chain events and receive a subscription ID."""
        url = f"{self.base_url}/wallets/events"
        payload = {"chain": chain, "filter_criteria": filter_criteria, "callback_url": callback_url}
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    async def list_event_subscriptions(self) -> List[Dict[str, Any]]:
        """List all on-chain event subscriptions."""
        url = f"{self.base_url}/wallets/events"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def unsubscribe_event(self, subscription_id: str) -> None:
        """Remove an on-chain event subscription."""
        url = f"{self.base_url}/wallets/events/{subscription_id}"
        response = await self.client.delete(url)
        response.raise_for_status()

    async def create_wallet(self, chain: str) -> Dict[str, Any]:
        response = await self.client.post("/wallets/", json={"chain": chain})
        response.raise_for_status()
        return response.json()

    async def import_wallet(self, chain: str, private_key: str) -> Dict[str, Any]:
        response = await self.client.post("/wallets/import", json={"chain": chain, "private_key": private_key})
        response.raise_for_status()
        return response.json()

    async def list_wallets(self) -> List[Dict[str, Any]]:
        response = await self.client.get("/wallets/")
        response.raise_for_status()
        return response.json()

    async def delete_wallet(self, wallet_id: str) -> None:
        response = await self.client.delete(f"/wallets/{wallet_id}")
        response.raise_for_status()

    async def get_token_balance(self, wallet_id: str, token_address: str) -> Dict[str, Any]:
        response = await self.client.get(f"/wallets/{wallet_id}/tokens/{token_address}/balance")
        response.raise_for_status()
        return response.json()

    async def transfer_tokens(self, wallet_id: str, token_address: str, to_address: str, amount: float) -> Dict[str, Any]:
        payload = {"token_address": token_address, "to_address": to_address, "amount": amount}
        response = await self.client.post(f"/wallets/{wallet_id}/tokens/transfer", json=payload)
        response.raise_for_status()
        return response.json()

    async def approve_tokens(self, wallet_id: str, token_address: str, spender_address: str, amount: float) -> Dict[str, Any]:
        payload = {"token_address": token_address, "spender_address": spender_address, "amount": amount}
        response = await self.client.post(f"/wallets/{wallet_id}/tokens/approve", json=payload)
        response.raise_for_status()
        return response.json()

    async def send_user_operation(self, user_op: Dict[str, Any], entry_point_address: str) -> Dict[str, Any]:
        payload = {"user_op": user_op, "entry_point_address": entry_point_address}
        response = await self.client.post("/wallets/account-ops/send", json=payload)
        response.raise_for_status()
        return response.json()

    async def get_user_operation_status(self, user_op_hash: str) -> Dict[str, Any]:
        response = await self.client.get(f"/wallets/account-ops/status/{user_op_hash}")
        response.raise_for_status()
        return response.json()
