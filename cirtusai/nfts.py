import requests
from typing import Dict, Any, List

class NftsClient:
    """
    Client for NFT operations: minting, batch transfers, metadata retrieval.
    """
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def list_nfts(self, wallet_id: str) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/nfts/{wallet_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_nft_metadata(self, contract_address: str, token_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/nfts/{contract_address}/{token_id}/metadata"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data[0] if isinstance(data, list) else data

    def mint_nft(self, contract_address: str, to_address: str, metadata_uri: str) -> Dict[str, Any]:
        url = f"{self.base_url}/nfts/{contract_address}/mint"
        payload = {"to_address": to_address, "metadata_uri": metadata_uri}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def batch_transfer(self, contract_address: str, transfers: List[Dict[str, Any]]) -> Dict[str, Any]:
        url = f"{self.base_url}/nfts/{contract_address}/batch-transfer"
        payload = {"transfers": transfers}
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def burn_nft(self, contract_address: str, token_id: str) -> None:
        url = f"{self.base_url}/nfts/{contract_address}/{token_id}/burn"
        resp = self.session.delete(url)
        resp.raise_for_status()
