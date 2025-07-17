import unittest
from unittest.mock import MagicMock, patch
from cirtusai.security import MonitoringClient, ComplianceClient

class TestMonitoringClient(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.client = MonitoringClient(self.session, "http://test.com")

    def test_watch_address(self):
        self.client.watch_address("0x123", "eth")
        self.session.post.assert_called_with(
            "http://test.com/monitoring/watch-address",
            params={"address": "0x123", "chain": "eth", "provider": "blocknative"},
        )
    def test_list_watches_and_alerts(self):
        # list_watches should call GET on /monitoring/watches
        self.client.list_watches()
        self.session.get.assert_called_with("http://test.com/monitoring/watches")
        # get_alerts should call GET on /monitoring/alerts
        self.client.get_alerts()
        self.session.get.assert_called_with("http://test.com/monitoring/alerts")

class TestComplianceClient(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.client = ComplianceClient(self.session, "http://test.com")

    def test_get_kyc_status(self):
        self.client.get_kyc_status()
        self.session.get.assert_called_with("http://test.com/compliance/kyc-status")

    def test_initiate_kyc(self):
        self.client.initiate_kyc()
        self.session.post.assert_called_with("http://test.com/compliance/initiate-kyc")
    def test_generate_report_and_audit_trail(self):
        # generate_report should GET with params
        self.client.generate_report('2025-01-01', '2025-01-31', 'full')
        self.session.get.assert_called_with(
            "http://test.com/compliance/report",
            params={"start_date": '2025-01-01', "end_date": '2025-01-31', "report_type": 'full'}
        )
        # get_audit_trail should GET the audit endpoint
        self.client.get_audit_trail('e1', 'wallet')
        self.session.get.assert_called_with("http://test.com/compliance/audit/wallet/e1")

if __name__ == "__main__":
    unittest.main()
