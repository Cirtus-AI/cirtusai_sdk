import pytest
import requests
from cirtusai.swap import SwapClient

class DummyResponse:
    def __init__(self, json_data=None, status_code=200):
        self._json = json_data or {}
        self.status_code = status_code
    def json(self):
        return self._json
    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError()

@pytest.fixture
def client(monkeypatch):
    session = requests.Session()
    monkeypatch.setattr(session, 'get', lambda url, params=None: DummyResponse({'quote': 'ok'}, 200))
    monkeypatch.setattr(session, 'post', lambda url, json=None: DummyResponse({'swap_id': 'xyz'}, 200))
    return SwapClient(session, 'http://api')

def test_quote_and_execute_and_cancel(client):
    quote = client.get_quote('eth', 'polygon', '0x0', '0x1', 1.0)
    assert quote['quote'] == 'ok'
    exec = client.execute_swap({'param': 'value'})
    assert exec['swap_id'] == 'xyz'
    # cancel should not raise
    client.cancel_swap('xyz')
