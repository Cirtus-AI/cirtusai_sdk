import requests
from typing import Dict, Any, List

class ChildAssetsClient:
    """
    Client for managing child-specific assets (CRUD operations).
    """
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def list_child_assets(self, child_id: str) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/child_assets"
        params = {"child_id": child_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_child_asset(self, asset_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/child_assets/{asset_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data[0] if isinstance(data, list) else data

    def create_child_asset(self, child_id: str, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/child_assets"
        payload = {"child_id": child_id, **asset_data}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def update_child_asset(self, asset_id: str, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/child_assets/{asset_id}"
        resp = self.session.put(url, json=asset_data)
        resp.raise_for_status()
        return resp.json()

    def delete_child_asset(self, asset_id: str) -> None:
        url = f"{self.base_url}/child_assets/{asset_id}"
        resp = self.session.delete(url)
        resp.raise_for_status()
