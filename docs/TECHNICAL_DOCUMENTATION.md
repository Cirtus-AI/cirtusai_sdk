# Technical Documentation

This document provides in-depth examples, API models, and edge-case handling for the CirtusAI Python SDK.

## Architecture Overview

The SDK is organized into the following modules:

```
CirtusAIClient
├── auth       # AuthClient (sync) & AsyncAuthClient
├── agents     # AgentsClient & AsyncAgentsClient
├── wallets    # WalletsClient & AsyncWalletsClient
├── identity   # IdentityClient & AsyncIdentityClient
└── schemas    # Pydantic models for typed requests/responses
```

## Pydantic Schemas

Located in `cirtusai/schemas.py`:

```python
class Agent(BaseModel):
    id: str
    name: Optional[str]
    did: Optional[str]
    state: Optional[dict]

class ChildAgent(BaseModel):
    id: str
    parent_id: Optional[str]
    name: Optional[str]
    permissions: Optional[dict]
    state: Optional[dict]

class Asset(BaseModel):
    id: str
    type: str
    details: dict

class EmailAccount(BaseModel):
    id: str
    provider: str
    email_address: str
    config: dict

class DID(BaseModel):
    did: str
    info: dict

class CredentialResponse(BaseModel):
    credential: dict
```

These models validate and serialize data returned from the API.

---

## Synchronous Clients

### Initialization

All sync clients share a `requests.Session`:

```python
from cirtusai import CirtusAIClient
client = CirtusAIClient(base_url, token="jwt-token")
```

### AuthClient

- `login(email: str, password: str) -> dict`
- `refresh(refresh_token: str) -> dict`

### AgentsClient

- `list_agents() -> List[Agent]`
- `get_agent(agent_id: str) -> Agent`
- `create_child_agent(parent_id: str, name: str) -> ChildAgent`
- `delete_agent(agent_id: str) -> None`
- `get_children() -> List[ChildAgent]`
- `update_child_permissions(child_id: str, permissions: dict) -> dict`
- `unlink_child_agent(child_id: str) -> None`
- `provision_email(child_id: str) -> dict`
- `provision_wallet(child_id: str, chain: str) -> dict`

### WalletsClient

- `list_assets() -> dict`
- `list_email_accounts() -> List[EmailAccount]`
- `create_email_account(provider: str, email_address: str, config: dict) -> EmailAccount`
- `update_email_account(account_id: str, provider: str, email_address: str, config: dict) -> EmailAccount`
- `delete_email_account(account_id: str) -> None`
- `refresh_email_token(account_id: str) -> dict`

### IdentityClient

- `get_did(agent_id: str) -> DID`
- `issue_credential(subject_id: str, types: List[str], claim: dict) -> CredentialResponse`
- `verify_credential(jwt_token: str) -> dict`

---

## Asynchronous Clients

Use `httpx.AsyncClient` under the hood:

```python
from cirtusai.async_.client import AsyncCirtusAIClient
client = AsyncCirtusAIClient(base_url, token)
data = await client.agents.list_agents()
await client.close()
```

The method signatures mirror the sync clients, returning `dict` or `List[dict]`.

---

## CLI Implementation

- Built with `click` in `cirtusai/cli.py`
- Entry point: `cirtusai` console script
- Subcommands:
  - `auth`: `login`, `refresh`
  - `agents`: `list`, `get`, `children`, `create-child`, `update-permissions`, `unlink`, `provision-email`, `provision-wallet`
  - `wallets`: `list-assets`, `list-email`, `create-email`, `update-email`, `delete-email`, `refresh-email-token`
  - `identity`: `get-did`, `issue-credential`, `verify-credential`

Example:

```bash
cirtusai agents list  # returns JSON array
```

---

## Error Handling & Retries

- HTTP 4xx and 5xx codes raise `requests.HTTPError` (sync) or `httpx.HTTPStatusError` (async).
- Consumers can catch these to inspect `.response.status_code` and `.response.json()`.

---

## Testing

Run all tests with:
```bash
pytest
```

Mocks are configured with:
- `responses` for sync
- `respx` for async

Each test suite is located in `tests/` (e.g. `test_client.py`, `test_async_client.py`, `test_agents_client.py`, `test_cli_agents.py`).
