import pytest
import responses
from cirtusai.client import CirtusAIClient
from responses.matchers import json_params_matcher

API_URL = "http://testserver"
TOKEN = "test-token"

@pytest.fixture
def client():
    return CirtusAIClient(base_url=API_URL, token=TOKEN)

@responses.activate
def test_list_agents(client):
    data = [{"id": "agent1"}, {"id": "agent2"}]
    responses.add(responses.GET, f"{API_URL}/agents", json=data, status=200)
    resp = client.agents.list_agents()
    assert resp == data

@responses.activate
def test_create_child_agent(client):
    payload = {"parent_id": "agent1", "name": "child"}
    data = {"id": "child1"}
    responses.add(
        responses.POST,
        f"{API_URL}/agents/children",
        json=data,
        status=201,
        match=[json_params_matcher(payload)]
    )
    resp = client.agents.create_child_agent("agent1", "child")
    assert resp == data

@responses.activate
def test_list_assets(client):
    data = {"assets": ["a", "b"]}
    responses.add(responses.GET, f"{API_URL}/wallets", json=data, status=200)
    resp = client.wallets.list_assets()
    assert resp == data

@responses.activate
def test_issue_credential(client):
    payload = {"subject_id": "sub", "type": ["VerifiableCredential"], "claim": {"k": "v"}}
    data = {"credential": "abc"}
    responses.add(
        responses.POST,
        f"{API_URL}/identity/credentials/issue",
        json=data,
        status=200,
        match=[json_params_matcher(payload)]
    )
    resp = client.identity.issue_credential("sub", ["VerifiableCredential"], {"k": "v"})
    assert resp == data
