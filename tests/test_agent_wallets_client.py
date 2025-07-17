import unittest
from unittest.mock import MagicMock
from cirtusai.wallets import WalletsClient

class TestAgentWalletsClient(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.client = WalletsClient(self.session, "http://api")

    def test_deploy_agent_wallet(self):
        self.client.deploy_agent_wallet()
        self.session.post.assert_called_with("http://api/agents/wallets/")

    def test_list_agent_wallets(self):
        self.client.list_agent_wallets()
        self.session.get.assert_called_with("http://api/agents/wallets/")

    def test_get_agent_wallet(self):
        address = "0xABC"
        self.client.get_agent_wallet(address)
        self.session.get.assert_called_with(f"http://api/agents/wallets/{address}")

    def test_set_spending_limit(self):
        address = "0xABC"
        self.client.set_spending_limit(address, "0xTOKEN", 1000, 86400)
        self.session.post.assert_called_with(
            f"http://api/agents/wallets/{address}/spending_limit",
            json={"token": "0xTOKEN", "amount": 1000, "period": 86400}
        )

    def test_update_whitelist(self):
        address = "0xABC"
        self.client.update_whitelist(address, "0xTARGET", True)
        self.session.post.assert_called_with(
            f"http://api/agents/wallets/{address}/whitelist",
            json={"target": "0xTARGET", "allowed": True}
        )

    def test_set_threshold(self):
        address = "0xABC"
        self.client.set_threshold(address, 500)
        self.session.post.assert_called_with(
            f"http://api/agents/wallets/{address}/threshold",
            json={"new_threshold": 500}
        )

    def test_list_wallet_transactions(self):
        address = "0xABC"
        self.client.list_wallet_transactions(address)
        self.session.get.assert_called_with(f"http://api/agents/wallets/{address}/transactions")

if __name__ == '__main__':
    unittest.main()
