import pytest
import requests
from cirtusai.nfts import NftsClient

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
    monkeypatch.setattr(session, 'get', lambda url: DummyResponse([{'token_id': '1'}], 200))
    monkeypatch.setattr(session, 'post', lambda url, json=None: DummyResponse({'minted': True}, 200))
    monkeypatch.setattr(session, 'delete', lambda url: DummyResponse({}, 204))
    return NftsClient(session, 'http://api')

def test_list_and_metadata_and_mint_and_batch_and_burn(client):
    nfts = client.list_nfts('wallet1')
    assert isinstance(nfts, list)
    meta = client.get_nft_metadata('contract', '1')
    assert isinstance(meta, dict)
    minted = client.mint_nft('contract', 'addr', 'uri')
    assert minted['minted'] is True
    batch = client.batch_transfer('contract', [{'to':'a','token_id':'1'}])
    assert 'transfers' in batch or isinstance(batch, dict)
    # burn should not raise
    client.burn_nft('contract', '1')
