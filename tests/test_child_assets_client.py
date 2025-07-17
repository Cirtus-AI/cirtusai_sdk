import pytest
import requests
from cirtusai.child_assets import ChildAssetsClient

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
    # list and get return list or dict
    monkeypatch.setattr(session, 'get', lambda url, params=None: DummyResponse([{'id':'a1'}]))
    monkeypatch.setattr(session, 'post', lambda url, json=None: DummyResponse({'id':'c1'}))
    monkeypatch.setattr(session, 'put', lambda url, json=None: DummyResponse({'updated': True}))
    monkeypatch.setattr(session, 'delete', lambda url: DummyResponse({}, 204))
    return ChildAssetsClient(session, 'http://api')

def test_list_and_get_and_create_and_update_and_delete(client):
    assets = client.list_child_assets('child1')
    assert isinstance(assets, list)
    asset = client.get_child_asset('a1')
    assert isinstance(asset, dict)
    created = client.create_child_asset('child1', {'foo':'bar'})
    assert created['id'] == 'c1'
    updated = client.update_child_asset('c1', {'foo':'baz'})
    assert updated['updated'] is True
    # delete should not raise
    client.delete_child_asset('c1')
