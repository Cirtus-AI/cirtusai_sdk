from typing import Dict, Any, List
from requests import Session

class MonitoringClient:
    def __init__(self, session: Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def watch_address(self, address: str, chain: str, provider: str = "blocknative") -> Dict[str, Any]:
        """Watch a given address on a specific chain for real-time transaction updates."""
        url = f"{self.base_url}/monitoring/watch-address"
        params = {"address": address, "chain": chain, "provider": provider}
        response = self.session.post(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_tx_status(self, tx_hash: str, provider: str = "blocknative") -> Dict[str, Any]:
        """Get the status of a transaction from the specified monitoring provider."""
        url = f"{self.base_url}/monitoring/tx-status/{tx_hash}"
        params = {"provider": provider}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    def get_transaction_status(self, tx_hash: str, provider: str = "blocknative") -> Dict[str, Any]:
        """Alias for get_tx_status, matching SDK naming."""
        return self.get_tx_status(tx_hash, provider)
    def list_watches(self) -> List[Dict[str, Any]]:
        """List all active address watches."""
        url = f"{self.base_url}/monitoring/watches"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Retrieve all generated alerts."""
        url = f"{self.base_url}/monitoring/alerts"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

class ComplianceClient:
    def __init__(self, session: Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def get_kyc_status(self) -> Dict[str, Any]:
        """Get the KYC status for the current user."""
        url = f"{self.base_url}/compliance/kyc-status"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def initiate_kyc(self) -> Dict[str, Any]:
        """Initiate the KYC verification flow for the current user."""
        url = f"{self.base_url}/compliance/initiate-kyc"
        response = self.session.post(url)
        response.raise_for_status()
        return response.json()
    def generate_report(self, start_date: str, end_date: str, report_type: str) -> Dict[str, Any]:
        """Generate a compliance report over a date range."""
        url = f"{self.base_url}/compliance/report"
        params = {"start_date": start_date, "end_date": end_date, "report_type": report_type}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    def get_audit_trail(self, entity_id: str, entity_type: str) -> Dict[str, Any]:
        """Retrieve audit trail for a given entity (e.g., wallet, agent)."""
        url = f"{self.base_url}/compliance/audit/{entity_type}/{entity_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()
