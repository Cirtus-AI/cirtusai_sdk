import unittest
from unittest.mock import MagicMock
from cirtusai.wallets import WalletsClient
from cirtusai.governance import GovernanceClient

class TestWalletsClient(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.client = WalletsClient(self.session, "http://test.com")

    def test_list_assets(self):
        self.client.list_assets()
        self.session.get.assert_called_with("http://test.com/wallets")

    def test_create_wallet(self):
        self.client.create_wallet("ethereum")
        self.session.post.assert_called_with("/wallets/", json={"chain": "ethereum"})

    def test_import_wallet(self):
        self.client.import_wallet("polygon", "0xPRIVATEKEY")
        self.session.post.assert_called_with("/wallets/import", json={"chain": "polygon", "private_key": "0xPRIVATEKEY"})

    def test_list_wallets(self):
        self.client.list_wallets()
        self.session.get.assert_called_with("/wallets/")

    def test_delete_wallet(self):
        self.client.delete_wallet("walletid")
        self.session.delete.assert_called_with("/wallets/walletid")

    def test_get_token_balance(self):
        self.client.get_token_balance("walletid", "0xTOKEN")
        self.session.get.assert_called_with("/wallets/walletid/tokens/0xTOKEN/balance")

    def test_transfer_tokens(self):
        self.client.transfer_tokens("walletid", "0xTOKEN", "0xTO", 10.0)
        self.session.post.assert_called_with("/wallets/walletid/tokens/transfer", json={"token_address": "0xTOKEN", "to_address": "0xTO", "amount": 10.0})

    def test_approve_tokens(self):
        self.client.approve_tokens("walletid", "0xTOKEN", "0xSPENDER", 100.0)
        self.session.post.assert_called_with("/wallets/walletid/tokens/approve", json={"token_address": "0xTOKEN", "spender_address": "0xSPENDER", "amount": 100.0})

    def test_send_user_operation(self):
        user_op = {"foo": "bar"}
        self.client.send_user_operation(user_op, "0xENTRY")
        self.session.post.assert_called_with("/wallets/account-ops/send", json={"user_op": user_op, "entry_point_address": "0xENTRY"})

    def test_get_user_operation_status(self):
        self.client.get_user_operation_status("0xHASH")
        self.session.get.assert_called_with("/wallets/account-ops/status/0xHASH")

    def test_subscribe_event(self):
        self.client.subscribe_event("ethereum", {"address": "0x..."}, "http://callback")
        self.session.post.assert_called_with("http://test.com/wallets/events", json={"chain": "ethereum", "filter_criteria": {"address": "0x..."}, "callback_url": "http://callback"})

    def test_list_event_subscriptions(self):
        self.client.list_event_subscriptions()
        self.session.get.assert_called_with("http://test.com/wallets/events")

    def test_unsubscribe_event(self):
        self.client.unsubscribe_event("subid")
        self.session.delete.assert_called_with("http://test.com/wallets/events/subid")

    def test_register_rwa_asset(self):
        self.client.register_rwa_asset("0xTOKEN", "1", "http://meta")
        self.session.post.assert_called_with("http://test.com/wallets/rwa", json={"token_address": "0xTOKEN", "token_id": "1", "metadata_uri": "http://meta"})

    def test_list_rwa_assets(self):
        self.client.list_rwa_assets()
        self.session.get.assert_called_with("http://test.com/wallets/rwa")

    def test_transfer_rwa_asset(self):
        self.client.transfer_rwa_asset("assetid", "0xTO")
        self.session.post.assert_called_with("http://test.com/wallets/rwa/assetid/transfer", json={"to_address": "0xTO"})

    def test_create_yield_strategy(self):
        self.client.create_yield_strategy("asset", "Aave", 5.0)
        self.session.post.assert_called_with("http://test.com/wallets/strategies", json={"asset_key": "asset", "protocol": "Aave", "min_apr": "5.0"})

    def test_list_yield_strategies(self):
        self.client.list_yield_strategies()
        self.session.get.assert_called_with("http://test.com/wallets/strategies")

    def test_run_yield_strategy(self):
        self.client.run_yield_strategy("stratid")
        self.session.post.assert_called_with("http://test.com/wallets/strategies/stratid/run")

class TestGovernanceClient(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.client = GovernanceClient(self.session, "http://test.com")

    def test_create_proposal(self):
        self.client.create_proposal([], [], [], "test")
        self.session.post.assert_called_with(
            "http://test.com/governance/proposals",
            json={"targets": [], "values": [], "calldatas": [], "description": "test"},
        )

    def test_cast_vote(self):
        self.client.cast_vote(1, 1)
        self.session.post.assert_called_with(
            "http://test.com/governance/vote", json={"proposal_id": 1, "support": 1}
        )

    def test_get_proposal_state(self):
        self.client.get_proposal_state(1)
        self.session.get.assert_called_with("http://test.com/governance/proposals/1")

if __name__ == "__main__":
    unittest.main()
