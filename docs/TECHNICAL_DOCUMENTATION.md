# Technical Documentation - 2FA ENFORCED

This document provides in-depth examples, API models, and edge-case handling for the CirtusAI Python SDK with **mandatory Two-Factor Authentication**.

## 🔒 Important: 2FA is ENFORCED

**All newly registered users MUST use 2FA.** The CirtusAI platform automatically sets up TOTP during registration and requires it for login. This SDK provides comprehensive support for:

- **Automatic 2FA setup** during registration
- **Two-step login flow** for production use
- **Direct login methods** for testing
- **TOTP management** and troubleshooting
- **Error handling** for 2FA scenarios

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

### AuthClient - 2FA ENFORCED

**All authentication now requires 2FA for new users:**

- `register(username, email, password, preferred_2fa_method="totp") -> TwoFactorSetupResponse`
  - **Automatically sets up 2FA** - returns QR code and backup codes
  - **No opt-out** - all new accounts require 2FA
- `login(username: str, password: str) -> Union[Token, TwoFactorRequiredResponse]`
  - **Legacy users**: May return Token directly
  - **New users**: Always returns TwoFactorRequiredResponse. `username` can be the username or email.
- `verify_2fa(temporary_token: str, totp_code: str) -> Token`
  - **Required second step** for 2FA users
- `refresh(refresh_token: str) -> Token`
- `get_2fa_status() -> TwoFactorStatusResponse`
- `debug_2fa() -> dict` - **Troubleshooting helper**

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

---

## 2FA Usage Examples

### Registration with Automatic 2FA Setup

```python
from cirtusai import CirtusAIClient

client = CirtusAIClient(base_url="http://localhost:8000")

# Register user - 2FA is automatically set up
setup_info = client.auth.register(
    username="newuser",
    email="user@example.com", 
    password="SecurePass123!",
    preferred_2fa_method="totp"
)

print(f"Secret: {setup_info.secret}")
print(f"QR Code URI: {setup_info.qr_code_uri}")
print(f"Backup Codes: {setup_info.backup_codes}")

# You can save the QR code image (base64 encoded) to a file
import base64
with open("qr_code.png", "wb") as f:
    f.write(base64.b64decode(setup_info.qr_code_image))
```

### Two-Step Login Flow

```python
# Step 1: Initial login
auth_response = client.auth.login("newuser", "SecurePass123!")

if hasattr(auth_response, 'requires_2fa') and auth_response.requires_2fa:
    # Step 2: Get TOTP code from user and verify
    totp_code = input("Enter 6-digit code from authenticator app: ")
    token_response = client.auth.verify_2fa(
        temporary_token=auth_response.temporary_token,
        totp_code=totp_code
    )
    client.set_token(token_response.access_token)
else:
    # Legacy user without 2FA
    client.set_token(auth_response.access_token)
```

### Direct Login with 2FA (for tests or scripts)

```python
# For non-interactive use - combine username, password and TOTP code
token_response = client.auth.login_with_2fa(
    "newuser",
    "SecurePass123!",
    "123456"  # Current 6-digit code from authenticator app
)
client.set_token(token_response.access_token)
```

### Troubleshooting 2FA

```python
# Get debug information for TOTP sync issues
debug_info = client.auth.debug_2fa()
print(f"Current valid codes: {debug_info['valid_codes']}")
print(f"Server time: {debug_info['current_server_time']}")
```

For complete examples, see `examples/2fa_examples.py` in the SDK repository.
