# CirtusAI Python SDK

**The Trust Layer for the Agent Economy** - v0.2.2 (beta)

Welcome to the official Python SDK for CirtusAI, the platform for building, managing, and securing autonomous AI agents. This SDK provides a comprehensive toolkit for developers to create sophisticated agents with blockchain-level security, multi-chain wallet support, and enterprise-grade compliance features.

Learn more about the CirtusAI vision at [cirtusai.com](https://cirtusai.com).

## Core Concepts

- **Master Agents**: Every user account is assigned a Master Agent, which acts as the central controller for all of that user's resources, including child agents and asset vaults.
- **Child Agents**: These are specialized agents created by a Master Agent. They operate with a limited, specific set of permissions that are delegated to them, ensuring they only perform authorized actions.
- **Permissions**: CirtusAI uses a granular, zero-trust permissioning engine. Child agents must be explicitly granted permissions (e.g., `email:read`, `wallet:send`) to interact with specific services or data.

## Features

- **Enterprise-Grade 2FA Security**: TOTP authentication with comprehensive security features.
- **Hierarchical Agent Management**: Create and manage master/child agent structures with granular, delegatable permissions.
- **Multi-Chain Wallets**: Full support for creating and managing wallets on Ethereum, Polygon, Arbitrum, and more.
- **Secure Email Integration**: AI-powered email processing with LangChain integration, secured by agent permissions.
- **Security & Compliance**: Built-in tools for KYC/AML verification, tamper-evident audit trails, and regulatory reporting.
- **Cross-Chain Bridging**: Seamlessly transfer assets across different blockchain networks.
- **DeFi & NFT Operations**: Integrate with DeFi protocols for token swaps and yield farming, or manage NFTs with full marketplace functionality.
- **Decentralized Identity**: Manage DIDs and issue Verifiable Credentials to agents and users.

## Installation

```bash
pip install cirtusai-sdk
```

## Quick Start: Creating Your First AI Agent

This guide will walk you through creating a simple child agent that can read and send emails.

### Step 1: Initialize the Client
First, import and initialize the `CirtusAIClient`, pointing it to your backend instance.

```python
from cirtusai import CirtusAIClient

# Initialize the client
client = CirtusAIClient(base_url="http://localhost:8000") # Or your production API URL
```

### Step 2: Authenticate
Log in to your CirtusAI account to get an access token. The SDK will automatically manage the token for subsequent requests.

```python
# Authenticate with your credentials
try:
    token_response = client.auth.login("your_username", "your_password")
    client.set_token(token_response.access_token)
    print("Authentication successful!")
except Exception as e:
    print(f"Authentication failed: {e}")
```

### Step 3: Get Your Master Agent
Child agents are created under a master agent. First, retrieve your primary master agent.

```python
try:
    master_agents = client.agents.list_agents()
    if not master_agents:
        raise Exception("No master agents found for this user.")
    
    # Select the first master agent as the parent
    master_agent_id = master_agents[0]['id']
    print(f"Using Master Agent ID: {master_agent_id}")
except Exception as e:
    print(f"Error fetching master agent: {e}")
```

### Step 4: Create a Child Agent
Now, create a new child agent and grant it permissions to read and send emails.

```python
try:
    child_agent = client.agents.create_child_agent(
        parent_id=master_agent_id,
        name="MyFirstEmailAgent",
        permissions_granted=["email:read", "email:send"]
    )
    child_agent_id = child_agent['id']
    print(f"Successfully created Child Agent: {child_agent}")
except Exception as e:
    print(f"Failed to create child agent: {e}")
```

### Step 5: Use the Agent to Send an Email
With the child agent created, you can now use its permissions to interact with services.

```python
try:
    # Use the child agent's ID to send an email
    result = client.email.send_email(
        agent_id=child_agent_id,
        recipient="test@example.com",
        subject="Hello from my CirtusAI Agent!",
        body="This email was sent programmatically using the CirtusAI SDK."
    )
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
```

## Documentation

For detailed guides, API references, and advanced examples, please see the `/docs` directory in this repository.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/YourFeature`).
3. Make your changes and add tests.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/YourFeature`).
6. Open a Pull Request.

## Support

- **Documentation**: Complete guides are available in the `/docs/` folder.
- **Examples**: Find sample code and complete workflows in the `/examples/` folder.
- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/Cirtus-AI/cirtusai_sdk/issues).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.