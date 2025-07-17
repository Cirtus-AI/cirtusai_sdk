import requests
from typing import Dict, Any, List

class MarketplaceClient:
    """
    Client for marketplace operations: listings, bids, orders.
    """
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def create_listing(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/marketplace/listings"
        resp = self.session.post(url, json=listing_data)
        resp.raise_for_status()
        return resp.json()

    def get_listing(self, listing_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/marketplace/listings/{listing_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data[0] if isinstance(data, list) else data

    def list_listings(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/marketplace/listings"
        resp = self.session.get(url, params=filters or {})
        resp.raise_for_status()
        return resp.json()

    def update_listing(self, listing_id: str, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/marketplace/listings/{listing_id}"
        resp = self.session.put(url, json=listing_data)
        resp.raise_for_status()
        return resp.json()

    def cancel_listing(self, listing_id: str) -> None:
        url = f"{self.base_url}/marketplace/listings/{listing_id}"
        resp = self.session.delete(url)
        resp.raise_for_status()

    def place_bid(self, listing_id: str, bid_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/marketplace/listings/{listing_id}/bids"
        resp = self.session.post(url, json=bid_data)
        resp.raise_for_status()
        return resp.json()

    def list_bids(self, listing_id: str) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/marketplace/listings/{listing_id}/bids"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def accept_bid(self, listing_id: str, bid_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/marketplace/listings/{listing_id}/bids/{bid_id}/accept"
        resp = self.session.post(url)
        resp.raise_for_status()
        return resp.json()
