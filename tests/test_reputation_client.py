import unittest
from unittest.mock import MagicMock, patch
from cirtusai.reputation import ReputationClient

class TestReputationClient(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.client = ReputationClient(self.session, "http://test.com")

    def test_issue_sbt(self):
        self.client.issue_sbt("0x123", "uri")
        self.session.post.assert_called_with(
            "http://test.com/reputation/issue-sbt",
            json={"to_address": "0x123", "token_uri": "uri"},
        )

    def test_get_sbt_owner(self):
        self.client.get_sbt_owner(1)
        self.session.get.assert_called_with("http://test.com/reputation/sbt-owner/1")

if __name__ == "__main__":
    unittest.main()
