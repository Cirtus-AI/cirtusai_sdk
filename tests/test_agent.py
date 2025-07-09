import pytest
import responses
from responses.matchers import json_params_matcher
from cirtusai.agent import CirtusAgent

API_URL = "http://testserver"
TOKEN = "test-token"
AGENT_ID = "agent-123"

@pytest.fixture
def client():
    return CirtusAgent(agent_id=AGENT_ID, token=TOKEN, base_url=API_URL)

@responses.activate
def test_list_assets(client):
    data = {"assets": ["asset1", "asset2"]}
    responses.add(responses.GET, f"{API_URL}/wallets", json=data, status=200)
    resp = client.list_assets()
    assert resp == data

@responses.activate
def test_provision_email(client):
    data = {"email": "user@example.com"}
    responses.add(responses.POST, f"{API_URL}/agents/children/{AGENT_ID}/assets/provision/email", json=data, status=200)
    resp = client.provision_email()
    assert resp == data

@responses.activate
def test_issue_credential(client):
    payload = {"subject_id": "sub-1", "type": ["VerifiableCredential"], "claim": {"foo": "bar"}}
    data = {"credential": "vc-data"}
    responses.add(
        responses.POST,
        f"{API_URL}/identity/credentials/issue",
        json=data,
        status=200,
        match=[json_params_matcher(payload)]
    )
    resp = client.issue_credential(subject_id="sub-1", types=["VerifiableCredential"], claim={"foo": "bar"})
    assert resp == data
