import requests
from typing import Dict, Any

class AuthClient:
    """
    Handles authentication: login with credentials and token refresh.
    """
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Obtain JWT access and refresh tokens via username/password."""
        url = f"{self.base_url}/auth/login"
        resp = self.session.post(url, json={"email": email, "password": password})
        resp.raise_for_status()
        return resp.json()

    def refresh(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh the access token using a valid refresh token."""
        url = f"{self.base_url}/auth/refresh"
        resp = self.session.post(url, json={"refresh_token": refresh_token})
        resp.raise_for_status()
        return resp.json()
