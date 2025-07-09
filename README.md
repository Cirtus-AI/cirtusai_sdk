# CirtusAI SDK

The **CirtusAI SDK** (Python) makes it trivial to integrate with the CirtusAI backend: create and manage agents, provision email and wallet assets, and issue/verify verifiable credentials.

## Installation

```bash
pip install cirtusai-sdk
```

Optional development extras (for running tests):

```bash
pip install cirtusai-sdk[dev]
```

## Quickstart

```python
from cirtusai import CirtusAIClient

# Initialize client (set token via env or pass directly)
client = CirtusAIClient(base_url="https://api.cirtus.ai", token="YOUR_ACCESS_TOKEN")

# List your master agents
agents = client.agents.list_agents()
print(agents)

# Create a child agent
child = client.agents.create_child_agent(parent_id=agents[0]["id"], name="MyChild")
print(child)

# Provision an email asset
email_asset = client.agents.provision_email(child["id"])
print(email_asset)

# Issue a verifiable credential
vc = client.identity.issue_credential(
    subject_id=child["id"],
    types=["VerifiableCredential"],
    claim={"role": "member"}
)
print(vc)

# Close client when done
client.close()
```

## Command-Line Interface

Once installed, you have the `cirtusai` command:

```bash
# Set environment variables for convenience:
export CIRTUSAI_TOKEN="..."
export CIRTUSAI_AGENT_ID="child-id"

# List agents
cirtusai agents list

# Provision an email asset
cirtusai agents provision-email
```

Run `cirtusai --help` for the full list of commands.

---

For comprehensive technical details, see the [Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md).
