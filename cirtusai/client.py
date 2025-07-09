import requests
from .auth import AuthClient
from .agents import AgentsClient
from .wallets import WalletsClient
from .identity import IdentityClient

class CirtusAIClient:
    """
    Synchronous client for CirtusAI: wraps sub-clients for auth, agents, wallets, and identity.
    """
    def __init__(self, base_url: str, token: str = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.auth = AuthClient(self.session, self.base_url)
        self.agents = AgentsClient(self.session, self.base_url)
        self.wallets = WalletsClient(self.session, self.base_url)
        self.identity = IdentityClient(self.session, self.base_url)

    def set_token(self, token: str):
        """Update the Authorization header with a new token."""
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def close(self):
        """Close underlying session."""
        self.session.close()
