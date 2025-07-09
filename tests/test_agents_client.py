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
    data = [{"id": "a1"}, {"id": "a2"}]
    responses.add(responses.GET, f"{API_URL}/agents", json=data, status=200)
    assert client.agents.list_agents() == data

@responses.activate
def test_get_agent(client):
    aid = "a1"
    data = {"id": aid}
    responses.add(responses.GET, f"{API_URL}/agents/{aid}", json=data, status=200)
    assert client.agents.get_agent(aid) == data

@responses.activate
def test_get_children(client):
    data = [{"id": "c1"}, {"id": "c2"}]
    responses.add(responses.GET, f"{API_URL}/agents/children", json=data, status=200)
    assert client.agents.get_children() == data

@responses.activate
def test_create_child_agent(client):
    payload = {"parent_id": "a1", "name": "child"}
    data = {"id": "c1"}
    responses.add(
        responses.POST,
        f"{API_URL}/agents/children",
        json=data,
        status=201,
        match=[json_params_matcher(payload)]
    )
    assert client.agents.create_child_agent("a1", "child") == data

@responses.activate
def test_update_permissions(client):
    child_id = "c1"
    perms = {"read": True}
    data = {"permissions": perms}
    responses.add(
        responses.PUT,
        f"{API_URL}/agents/children/{child_id}/permissions",
        json=data,
        status=200,
        match=[json_params_matcher({"permissions": perms})]
    )
    assert client.agents.update_child_permissions(child_id, perms) == data

@responses.activate
def test_unlink_child_agent(client):
    child_id = "c1"
    responses.add(responses.DELETE, f"{API_URL}/agents/children/{child_id}", status=204)
    # Should not raise
    client.agents.unlink_child_agent(child_id)

@responses.activate
def test_provision_email_and_wallet(client):
    child_id = "c1"
    e_data = {"email": "u@example.com"}
    w_data = {"wallet": "w1"}
    responses.add(responses.POST, f"{API_URL}/agents/children/{child_id}/assets/provision/email", json=e_data, status=200)
    responses.add(responses.POST, f"{API_URL}/agents/children/{child_id}/assets/provision/wallet", json=w_data, status=200)
    assert client.agents.provision_email(child_id) == e_data
    assert client.agents.provision_wallet(child_id, "ethereum") == w_data
