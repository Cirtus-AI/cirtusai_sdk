# agent.py
# Provides CirtusAgent: a lightweight wrapper for interacting with a single agent via REST, used by executor and example flows.
# 
import requests


class CirtusAgent:
    def __init__(self, agent_id: str, token: str, base_url: str):
        self.agent_id = agent_id
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def list_assets(self):
        resp = requests.get(f"{self.base_url}/wallets", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def list_master_agent(self):
        resp = requests.get(f"{self.base_url}/agents/{self.agent_id}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def provision_email(self):
        url = f"{self.base_url}/agents/children/{self.agent_id}/assets/provision/email"
        resp = requests.post(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def provision_wallet(self, chain: str):
        url = f"{self.base_url}/agents/children/{self.agent_id}/assets/provision/wallet"
        payload = {"chain": chain}
        resp = requests.post(url, json=payload, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def command(self, text: str):
        url = f"{self.base_url}/agents/{self.agent_id}/command"
        payload = {"text": text}
        resp = requests.post(url, json=payload, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def list_email_accounts(self):
        resp = requests.get(f"{self.base_url}/email/accounts", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def create_email_account(self, provider: str, email_address: str, config: dict):
        url = f"{self.base_url}/email/accounts"
        payload = {"provider": provider, "email_address": email_address, "config": config}
        resp = requests.post(url, json=payload, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def issue_credential(self, subject_id: str, types: list, claim: dict):
        url = f"{self.base_url}/identity/credentials/issue"
        payload = {"subject_id": subject_id, "type": types, "claim": claim}
        resp = requests.post(url, json=payload, headers=self.headers)
        resp.raise_for_status()
        return resp.json()
