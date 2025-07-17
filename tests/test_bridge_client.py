import unittest
from unittest.mock import MagicMock, patch
from cirtusai.bridge import BridgeClient, AssetsClient

class TestBridgeClient(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.client = BridgeClient(self.session, "http://test.com")

    def test_get_quote(self):
        self.client.get_quote("eth", "poly", "usdc", "usdc", 100)
        self.session.post.assert_called_with(
            "http://test.com/wallets/bridge/quote",
            json={
                "from_chain": "eth",
                "to_chain": "poly",
                "from_token": "usdc",
                "to_token": "usdc",
                "amount": 100,
            },
        )

class TestAssetsClient(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.client = AssetsClient(self.session, "http://test.com")

    def test_get_multi_chain_asset_view(self):
        self.client.get_multi_chain_asset_view()
        self.session.get.assert_called_with("http://test.com/wallets/assets/view")

    def test_refresh_multi_chain_asset_view(self):
        self.client.refresh_multi_chain_asset_view()
        self.session.post.assert_called_with("http://test.com/wallets/assets/refresh")

if __name__ == "__main__":
    unittest.main()
