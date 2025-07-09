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

```python
from cirtusai import CirtusAIClient

# Initialize client (set API_TOKEN env or pass explicitly)
client = CirtusAIClient(base_url="https://api.cirtus.ai", token="YOUR_JWT_TOKEN")

# Create a child agent under your master agent
child = client.agents.create_child_agent(parent_id="master-did", name="MyChild")
print("New child agent:", child)

# Provision an email asset for that child
email_asset = client.agents.provision_email(child["id"])
print("Email asset:", email_asset)

# Issue a verifiable credential
vc = client.identity.issue_credential(
    subject_id=child["id"],
    types=["VerifiableCredential"],
    claim={"role": "member"}
)
print("Issued VC:", vc)
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
- `login(email, password)` → `{ access_token, refresh_token, expires_in, ... }`
- `refresh(refresh_token)` → `{ access_token, ... }`

### AgentsClient
- `list_agents()` → `[ { id, name?, did?, state? }, ... ]`
- `get_agent(agent_id)` → `{ id, name, did, state }
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
- `issue_credential(subject_id, types, claim)` → `{ credential }
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

Under `cirtusai.schemas`:
- `Agent`, `ChildAgent`, `Asset`, `EmailAccount`, `Permissions`, `DID`, `CredentialResponse`

Use them to validate and serialize data in your own code:

```python
from cirtusai.schemas import Agent
agent = Agent(**client.agents.get_agent(id))
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
