import pytest  # noqa: F401
import respx  # type: ignore
from httpx import Response
from cirtusai.async_.client import AsyncCirtusAIClient

API_URL = "http://testserver"
TOKEN = "test-token"

@pytest.fixture
def event_loop():
    """Override event_loop for pytest-asyncio"""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_async_list_agents():
    client = AsyncCirtusAIClient(base_url=API_URL, token=TOKEN)
    async with respx.mock(base_url=API_URL) as route:
        route.get("/agents").respond(200, json=[{"id":"a1"}, {"id":"a2"}])
        data = await client.agents.list_agents()
        assert data == [{"id":"a1"}, {"id":"a2"}]
    await client.close()

@pytest.mark.asyncio
async def test_async_create_child_agent():
    client = AsyncCirtusAIClient(base_url=API_URL, token=TOKEN)
    async with respx.mock(base_url=API_URL) as route:
        payload = {"parent_id": "a1", "name": "child"}
        route.post("/agents/children", json=payload).respond(201, json={"id":"c1"})
        data = await client.agents.create_child_agent("a1", "child")
        assert data == {"id": "c1"}
    await client.close()

@pytest.mark.asyncio
async def test_async_list_assets():
    client = AsyncCirtusAIClient(base_url=API_URL, token=TOKEN)
    async with respx.mock(base_url=API_URL) as route:
        route.get("/wallets").respond(200, json={"assets": ["x", "y"]})
        data = await client.wallets.list_assets()
        assert data == {"assets": ["x", "y"]}
    await client.close()

@pytest.mark.asyncio
async def test_async_issue_credential():
    client = AsyncCirtusAIClient(base_url=API_URL, token=TOKEN)
    async with respx.mock(base_url=API_URL) as route:
        payload = {"subject_id": "s1", "type": ["VerifiableCredential"], "claim": {"k":"v"}}
        route.post("/identity/credentials/issue", json=payload).respond(200, json={"credential":"abc"})
        data = await client.identity.issue_credential("s1", ["VerifiableCredential"], {"k":"v"})
        assert data == {"credential": "abc"}
    await client.close()
