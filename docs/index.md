# CirtusAI Python SDK

**The Trust Layer for the Agent Economy** - v0.2.2 (beta)

>A comprehensive Python SDK for building autonomous AI agents with blockchain-level security, multi-chain wallets, and enterprise compliance features.

Learn more at [cirtusai.com](https://cirtusai.com) or view source on [GitHub](https://github.com/Cirtus-AI/cirtusai_sdk).

## Installation

```bash
pip install cirtusai-sdk
```

## Quick Start

```python
from cirtusai import CirtusAIClient

# Initialize client and authenticate
client = CirtusAIClient("https://api.cirtusai.com")
token = client.auth.login_with_2fa("username", "password", "123456")
client.set_token(token.access_token)

# Create an agent and provision email
agent = client.agents.create_child_agent(
    parent_id="master_agent_id",
    name="My Agent",
    permissions_granted=["email:read", "email:send"]
)
email_asset = client.agents.provision_email(agent['id'])
```

## Documentation

### Complete Guides

- **[Quick Start Guide](docs/quickstart.md)** - Get up and running in 5 minutes
- **[Authentication Guide](docs/authentication.md)** - 2FA setup, login flows, and security best practices
- **[Agent Management](docs/agents.md)** - Create, configure, and manage agents with permissions
- **[Wallet Operations](docs/wallets.md)** - Multi-chain wallets, transactions, and DeFi features
- **[Email Services](docs/email.md)** - AI-powered email processing and automation
- **[Security & Compliance](docs/security.md)** - KYC/AML, audit trails, and regulatory features
- **[Blockchain Infrastructure](docs/blockchain.md)** - Bridging, swaps, NFTs, governance, and identity


### Core Modules

| Module | Purpose | Key Features |
|--------|---------|--------------|
| `client.auth` | Authentication | 2FA, TOTP, login flows |
| `client.agents` | Agent Management | Create agents, permissions, provisioning |
| `client.wallets` | Wallet Operations | Multi-chain, transactions, DeFi |
| `client.email` | Email Services | AI processing, automation |
| `client.security` | Compliance | KYC/AML, monitoring, audit trails |
| `client.bridge` | Cross-Chain | Asset bridging, multi-chain views |
| `client.swap` | DeFi Swaps | Token exchanges, DEX integration |
| `client.nfts` | NFT Operations | Minting, transfers, metadata |
| `client.marketplace` | NFT Trading | Listings, bids, marketplace |
| `client.governance` | DAO Features | Proposals, voting, governance |
| `client.identity` | Digital Identity | DIDs, credentials, verification |
| `client.reputation` | Social Proof | Soulbound tokens, reputation |

## Command Line Interface

The SDK includes a comprehensive CLI for all operations:

```bash
# Authentication
cirtusai auth login --username myuser --enable-2fa

# Agent management  
cirtusai agents create-child --parent-id master_123 --name "Trading Agent"

# Wallet operations
cirtusai wallets create --chain ethereum

# Email processing
cirtusai email read-inbox --agent-id agent_123

# Compliance checks
cirtusai security kyc-status

# Cross-chain operations
cirtusai bridge get-quote --from ethereum --to polygon --token ETH --amount 1.0
```

See `cirtusai --help` for complete command reference.

## Examples

### Agent + Email Automation
```python
# Create agent with email processing
agent = client.agents.create_child_agent(
    parent_id="master_123",
    name="Email Assistant",
    permissions_granted=["email:read", "email:send"]
)

# Provision email capability
email_asset = client.agents.provision_email(agent['id'])

# Process emails with AI
from langchain_deepseek import ChatDeepSeek
llm = ChatDeepSeek(api_key="your_key")

messages = client.email.read_inbox(agent['id'])
for message in messages:
    summary = llm.invoke(f"Summarize: {message['text_body']}").content
    print(f"Summary: {summary}")
```

## Development

### Environment Setup
```bash
git clone https://github.com/cirtusai/cirtusai-sdk
cd cirtusai-sdk
pip install -e .
```

### Testing
```bash
# Run all tests
pytest

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

- **Documentation**: Complete guides in `/docs/`
- **API Reference**: Detailed method documentation in each guide
- **Examples**: Sample code and workflows
- **Issues**: Report bugs on GitHub
- **Community**: Join our Discord for support

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Changelog

### v0.2.2 (Latest)
- Added comprehensive security and compliance features
- Enhanced agent wallet functionality
- Improved cross-chain bridging
- Added marketplace operations
- Enhanced documentation and examples

### v0.2.1
- Added email services with AI integration
- Enhanced 2FA security features
- Added governance and identity modules
- Improved error handling

### v0.2.0
- Initial release with core features
- Basic authentication and agent management
- Wallet operations and DeFi integration
- CLI interface
