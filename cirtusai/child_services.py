import requests
from typing import Dict, Any, List

class ChildServicesClient:
    """
    Client for managing child agent services (microservices/endpoints dedicated to child agents).
    """
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def list_services(self, child_id: str) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/child_services"
        params = {"child_id": child_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_service(self, service_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/child_services/{service_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def create_service(self, child_id: str, service_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/child_services"
        payload = {"child_id": child_id, **service_data}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def update_service(self, service_id: str, service_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/child_services/{service_id}"
        resp = self.session.put(url, json=service_data)
        resp.raise_for_status()
        return resp.json()

    def delete_service(self, service_id: str) -> None:
        url = f"{self.base_url}/child_services/{service_id}"
        resp = self.session.delete(url)
        resp.raise_for_status()
        return None
