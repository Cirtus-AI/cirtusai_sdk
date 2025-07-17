import pytest
import requests
from cirtusai.marketplace import MarketplaceClient

class DummyResponse:
    def __init__(self, json_data=None, status_code=200):
        self._json = json_data or {}
        self.status_code = status_code
    def json(self):
        return self._json
    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error")

@pytest.fixture
def client(monkeypatch):
    session = requests.Session()
    monkeypatch.setattr(session, 'post', lambda url, json=None: DummyResponse({'id': '123'}, 200))
    monkeypatch.setattr(session, 'get', lambda url, params=None: DummyResponse([{'id': '123'}], 200))
    monkeypatch.setattr(session, 'put', lambda url, json=None: DummyResponse({'updated': True}, 200))
    monkeypatch.setattr(session, 'delete', lambda url: DummyResponse({}, 204))
    return MarketplaceClient(session, 'http://api')

def test_create_and_get_listing(client):
    data = client.create_listing({'name': 'Item'})
    assert data['id'] == '123'
    listing = client.get_listing('123')
    assert listing['id'] == '123'

def test_listings_and_update_and_cancel(client):
    listings = client.list_listings()
    assert isinstance(listings, list)
    updated = client.update_listing('123', {'price': 10})
    assert updated['updated'] is True
    # cancel should not raise
    client.cancel_listing('123')

def test_place_and_list_and_accept_bid(client):
    bid = client.place_bid('123', {'amount': 5})
    assert bid['id'] == '123'
    bids = client.list_bids('123')
    assert isinstance(bids, list)
    accepted = client.accept_bid('123', 'bid1')
    assert accepted['id'] == '123'
