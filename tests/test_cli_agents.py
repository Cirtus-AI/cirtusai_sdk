import os
import json
import pytest
from click.testing import CliRunner
import responses
from cirtusai.cli import main

# Stub out CirtusAIClient for CLI tests
def make_dummy_agent_client():
    class DummyAgents:
        def list_agents(self): return [{"id": "a1"}]
        def get_agent(self, aid): return {"id": aid}
        def get_children(self): return [{"id": "c1"}]
        def create_child_agent(self, pid, name): return {"id": "new_child", "parent_id": pid, "name": name}
        def update_child_permissions(self, cid, perms): return {"permissions": perms}
        def unlink_child_agent(self, cid): return None
    class DummyClient:
        def __init__(self, base_url, token):
            self.agents = DummyAgents()
    return DummyClient

@pytest.fixture(autouse=True)
def patch_client(monkeypatch):
    # Monkey patch CirtusAIClient in CLI module
    monkeypatch.setenv('CIRTUSAI_TOKEN', 'token123')
    monkeypatch.setenv('CIRTUSAI_AGENT_ID', 'c1')
    monkeypatch.setattr('cirtusai.cli.CirtusAIClient', make_dummy_agent_client())

def test_cli_list_agents():
    runner = CliRunner()
    result = runner.invoke(main, ['agents', 'list'])
    assert result.exit_code == 0
    assert '[{"id": "a1"}]' in result.output

def test_cli_get_agent():
    runner = CliRunner()
    result = runner.invoke(main, ['agents', 'get', 'a1'])
    assert result.exit_code == 0
    assert '{"id": "a1"}' in result.output

def test_cli_get_children():
    runner = CliRunner()
    result = runner.invoke(main, ['agents', 'children'])
    assert result.exit_code == 0
    assert '[{"id": "c1"}]' in result.output

def test_cli_create_child():
    runner = CliRunner()
    result = runner.invoke(main, ['agents', 'create-child', 'a1', 'child_name'])
    assert result.exit_code == 0
    assert 'new_child' in result.output

def test_cli_update_permissions():
    runner = CliRunner()
    perms = '{"read": true}'
    result = runner.invoke(main, ['agents', 'update-permissions', 'c1', perms])
    assert result.exit_code == 0
    assert '"read": true' in result.output

def test_cli_unlink_child():
    runner = CliRunner()
    result = runner.invoke(main, ['agents', 'unlink', 'c1'])
    assert result.exit_code == 0
    assert 'Unlinked child agent c1' in result.output
