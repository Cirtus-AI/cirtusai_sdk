import requests
import functools
from .auth import AuthClient
from .agents import AgentsClient
from .wallets import WalletsClient
from .identity import IdentityClient
from .governance import GovernanceClient
from .reputation import ReputationClient
from .bridge import BridgeClient, AssetsClient
from .security import MonitoringClient, ComplianceClient
from .email import EmailClient
from .marketplace import MarketplaceClient
from .swap import SwapClient
from .nfts import NftsClient
from .child_assets import ChildAssetsClient
class CirtusAIClient:
    """
    Synchronous client for CirtusAI: wraps sub-clients for auth, agents, wallets, and identity.
    """
    def __init__(self, base_url: str, token: str = None, **kwargs):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

        # Allow passing custom requests options like timeout
        if kwargs:
            self.session.request = functools.partial(self.session.request, **kwargs)

        self.auth = AuthClient(self.session, self.base_url)
        self.agents = AgentsClient(self.session, self.base_url)
        self.wallets = WalletsClient(self.session, self.base_url)
        self.identity = IdentityClient(self.session, self.base_url)
        self.governance = GovernanceClient(self.session, self.base_url)
        self.reputation = ReputationClient(self.session, self.base_url)
        self.bridge = BridgeClient(self.session, self.base_url)
        self.assets = AssetsClient(self.session, self.base_url)
        self.marketplace = MarketplaceClient(self.session, self.base_url)
        self.swap = SwapClient(self.session, self.base_url)
        self.nfts = NftsClient(self.session, self.base_url)
        self.child_assets = ChildAssetsClient(self.session, self.base_url)
        self.monitoring = MonitoringClient(self.session, self.base_url)
        self.compliance = ComplianceClient(self.session, self.base_url)
        self.email = EmailClient(self.session, self.base_url)

    def set_token(self, token: str):
        """Update the Authorization header with a new token."""
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    @property
    def token(self) -> str:
        """Return the current authorization token from the session header."""
        auth_header = self.session.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:]
        return None

    def close(self):
        """Close underlying session."""
        self.session.close()
