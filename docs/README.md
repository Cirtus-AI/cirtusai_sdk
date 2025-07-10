# CirtusAI Python SDK Documentation

Welcome to the CirtusAI Python SDK! This library wraps the CirtusAI REST API into simple, opinionated Python classes and a CLI, so you can integrate identity, agent, and wallet management into your applications in just a few lines of code.

---

## Table of Contents

- [Installation](#installation)
- [Quickstart](#quickstart)
- [Synchronous Client Reference](#synchronous-client-reference)
  - [CirtusAIClient](#cirtusaiclient)
  - [AuthClient](#authclient)
  - [AgentsClient](#agentsclient)
  - [WalletsClient](#walletsclient)
  - [IdentityClient](#identityclient)
- [Asynchronous Client](#asynchronous-client)
- [Command-Line Interface (CLI)](#command-line-interface-cli)
- [Pydantic Schemas](#pydantic-schemas)
- [Testing](#testing)
- [Publishing to PyPI](#publishing-to-pypi)

---

## Installation

```bash
pip install cirtusai-sdk
# or to install the dev extras:
pip install cirtusai-sdk[dev]
```

This will install:
- `requests` for synchronous HTTP
- `httpx` for async HTTP
- `click` for the CLI
- `pytest`, `responses`, `respx` for development/testing

---

## Quickstart

The recommended way to authenticate is using the two-step 2FA login flow.

```python
from cirtusai import CirtusAIClient
from cirtusai.auth import TwoFactorAuthenticationError

# Initialize client
client = CirtusAIClient(base_url="http://localhost:8000")

# Step 1: Log in with username and password
login_result = client.auth.login("myuser", "SecurePass123!")

# Step 2: If 2FA is required, verify with a TOTP code
if hasattr(login_result, 'requires_2fa') and login_result.requires_2fa:
    totp_code = input("Enter your 6-digit code: ")
    try:
        token = client.auth.verify_2fa(login_result.temporary_token, totp_code)
        client.set_token(token.access_token)
    except TwoFactorAuthenticationError as e:
        print(f"2FA verification failed: {e}")
else:
    # For accounts without 2FA enabled
    client.set_token(login_result.access_token)

# You can now use the authenticated client
if client.token:
    agents = client.agents.list_agents()
    print("Successfully fetched agents:", agents)

client.close()
```

---

## Synchronous Client Reference

### CirtusAIClient

```python
client = CirtusAIClient(base_url: str, token: Optional[str] = None)
# attributes:
#   .auth      -> AuthClient
#   .agents    -> AgentsClient
#   .wallets   -> WalletsClient
#   .identity  -> IdentityClient
# methods:
#   set_token(token: str)  # update auth header
#   close()
```

### AuthClient

- `register(username, email, password, preferred_2fa_method?)` -> `TwoFactorSetupResponse`
- `login(username, password)` → `Token` or `TwoFactorRequiredResponse`. `username` can be the username or email.
- `login_with_2fa(username, password, totp_code)` -> `Token`. `username` can be the username or email.
- `verify_2fa(temporary_token, totp_code)` -> `Token`
- `refresh(refresh_token)` → `Token`
- `get_2fa_status()` -> `TwoFactorStatusResponse`
- `setup_2fa()` -> `TwoFactorSetupResponse`
- `confirm_2fa(totp_code)` -> `{ message }`
- `disable_2fa(totp_code, password)` -> `{ message }`
- `debug_2fa()` -> `{ ...debug info... }`

### AgentsClient

- `list_agents()` → `[ { id, name?, did?, state? }, ... ]`
- `get_agent(agent_id)` → `{ id, name, did, state }`
- `create_child_agent(parent_id, name)` → `{ id, parent_id, name, state }`
- `delete_agent(agent_id)`
- `get_children()` → `[ ChildAgent, ... ]`
- `update_child_permissions(child_id, permissions)` → `{ permissions }`
- `unlink_child_agent(child_id)`
- `provision_email(child_id)` → `{ ...email asset... }`
- `provision_wallet(child_id, chain)` → `{ ...wallet asset... }`

### WalletsClient

- `list_assets()` → `{ assets: [...] }`
- `list_email_accounts()` → `[ EmailAccount, ... ]`
- `create_email_account(provider, email_address, config)` → `EmailAccount`
- `update_email_account(account_id, provider, email_address, config)` → `EmailAccount`
- `delete_email_account(account_id)`
- `refresh_email_token(account_id)` → `{ access_token, ... }`

### IdentityClient

- `get_did(agent_id)` → `DID` record
- `issue_credential(subject_id, types, claim)` → `{ credential }`
- `verify_credential(jwt_token)` → `{ verified: bool, payload: ... }`

---

## Asynchronous Client

All of the above clients also exist under `cirtusai.async_`:

```python
from cirtusai.async_.client import AsyncCirtusAIClient

client = AsyncCirtusAIClient(base_url, token)
await client.agents.list_agents()
await client.agents.provision_email(child_id)
await client.close()
```


---

## Command-Line Interface (CLI)

Once installed, run `cirtusai --help` for a full list of commands:

```bash
# set env vars or pass --token/--api-url
export CIRTUSAI_TOKEN="..."
export CIRTUSAI_AGENT_ID="child-id"

# Agents
cirtusai agents list
cirtusai agents get <agent_id>

# Child agents
cirtusai agents children
cirtusai agents create-child <parent> <name>
cirtusai agents update-permissions <child> '{"read": true}'

# Wallets
cirtusai wallets list-assets
cirtusai wallets list-email

# Identity
cirtusai identity get-did <agent_id>
cirtusai identity issue-credential <subject_id> '{"foo":"bar"}'
```

---

## Pydantic Schemas

The SDK uses Pydantic for all request and response data validation. Key schemas are available under `cirtusai.schemas`:

- **Authentication & 2FA:**
  - `Token`: Contains `access_token`, `refresh_token`, and `token_type`.
  - `UserRegister`: The model for creating a new user.
  - `TwoFactorSetupResponse`: Contains the secret, QR code, and backup codes for 2FA setup.
  - `TwoFactorRequiredResponse`: Indicates that a TOTP code is needed to complete login.
  - `TwoFactorVerifyRequest`: The request to verify a TOTP code.
  - `TwoFactorStatusResponse`: The current 2FA status of an account.
  - `TwoFactorDisableRequest`: The request to disable 2FA.
- **Core Models:**
  - `Agent`, `ChildAgent`, `Asset`, `EmailAccount`, `Permissions`, `DID`, `CredentialResponse`

Use them to validate and serialize data in your own code:

```python
from cirtusai.schemas import Agent, Token

# Example of how you might use the schemas in your application
# agent_data = client.agents.get_agent(id)
# agent = Agent.model_validate(agent_data)
#
# login_data = client.auth.login("user", "pass")
# if isinstance(login_data, dict):
#   token = Token.model_validate(login_data)
```

---

## Testing

To set up a development environment and run tests:

```bash
pip install -e .[dev]
pytest
```

- The `-e .[dev]` flag installs the SDK in editable mode with all development dependencies (see `setup.py`).
- Tests are located in the `tests/` directory and use `pytest`, `pytest-asyncio`, `responses`, and `respx`.

---

## Publishing to PyPI

This SDK is now maintained in its own repository: [https://github.com/cirtus-ai/cirtusai-sdk](https://github.com/cirtus-ai/cirtusai-sdk)

Publishing is automated via GitHub Actions on any new `vX.Y.Z` tag:

- Build step: `python -m build --sdist --wheel`
- Publish: `pypa/gh-action-pypi-publish`

To publish a new version:

1. Update the version in `setup.py`.
2. Commit and push your changes.
3. Tag the release:

   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

4. Ensure you have a `PYPI_API_TOKEN` in GitHub Secrets (see the technical documentation for details).

---

Happy coding with CirtusAI! 🎉
