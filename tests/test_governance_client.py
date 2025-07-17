import unittest
from unittest.mock import MagicMock, patch
from cirtusai.governance import GovernanceClient

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
