# CirtusAI SDK Quick Start Guide

## Installation

```bash
pip install cirtusai-sdk
```

## Basic Setup

```python
from cirtusai import CirtusAIClient

# Initialize client
client = CirtusAIClient("https://api.cirtusai.com")

# Authenticate
token = client.auth.login("your_username", "your_password")
client.set_token(token.access_token)
```

## 5-Minute Examples

### 1. Create and Use an Agent (2 minutes)

```python
# Create a child agent
agent = client.agents.create_child_agent(
    parent_id="your_master_agent_id",
    name="My First Agent",
    permissions_granted=["email:read", "email:send"]
)

# Provision email for the agent
email_asset = client.agents.provision_email(agent['id'])
print(f"Agent email: {email_asset['email_address']}")

# Read emails
messages = client.email.read_inbox(agent['id'])
print(f"Found {len(messages)} messages")
```

### 2. Create and Fund a Wallet (1 minute)

```python
# Create wallet
wallet = client.wallets.create_wallet("ethereum")
print(f"Wallet address: {wallet['address']}")

# Check balance
balance = client.wallets.get_balance("ethereum", wallet['address'])
print(f"ETH balance: {balance}")
```

### 3. Bridge Assets Cross-Chain (2 minutes)

```python
# Get bridge quote
quote = client.bridge.get_quote(
    from_chain="ethereum",
    to_chain="polygon", 
    from_token="ETH",
    to_token="MATIC",
    amount=1000000000000000000  # 1 ETH
)

print(f"Will receive: {quote['estimated_output']} MATIC")

# Execute bridge (if you have funds)
# bridge_result = client.bridge.bridge_transfer(...)
```

## Common Workflows

### Email + AI Processing

```python
from langchain_deepseek import ChatDeepSeek

# Setup AI
llm = ChatDeepSeek(api_key="your_deepseek_key")

# Process emails with AI
messages = client.email.read_inbox("agent_id")
for message in messages:
    summary = llm.invoke(f"Summarize: {message['text_body']}").content
    print(f"From: {message['from']}")
    print(f"Summary: {summary}")
```

### DeFi Operations

```python
# Get swap quote
quote = client.swap.get_quote(
    from_chain="ethereum",
    to_chain="ethereum",
    from_token="USDC", 
    to_token="ETH",
    amount=1000.0
)

# Execute swap
swap_result = client.swap.execute_swap({
    "from_token": "USDC",
    "to_token": "ETH", 
    "amount": 1000.0,
    "slippage_tolerance": 0.5
})
```

### NFT Management

```python
# List your NFTs
nfts = client.nfts.list_nfts("wallet_id")

# Create marketplace listing
listing = client.marketplace.create_listing({
    "nft_contract": nfts[0]['contract_address'],
    "token_id": nfts[0]['token_id'],
    "price": "0.1",
    "currency": "ETH"
})
```

## Error Handling

```python
try:
    result = client.some_operation()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 403:
        print("Permission denied")
    elif e.response.status_code == 401:
        print("Authentication required")
    else:
        print(f"Error: {e}")
```

## Next Steps

1. **Read the full documentation**: Explore detailed guides for each component
2. **Set up 2FA**: Enable two-factor authentication for security
3. **Create agent workflows**: Build complex automation with multiple agents
4. **Integrate with LangChain**: Add AI capabilities to your agents
5. **Explore DeFi**: Use cross-chain bridging and swapping features

## Quick Reference

### Core Modules

- `client.auth` - Authentication and 2FA
- `client.agents` - Agent management  
- `client.wallets` - Wallet and asset operations
- `client.email` - Email services
- `client.security` - KYC/AML compliance
- `client.bridge` - Cross-chain bridging
- `client.swap` - DeFi swaps
- `client.nfts` - NFT operations
- `client.marketplace` - NFT marketplace
- `client.governance` - DAO governance
- `client.identity` - Decentralized identity
- `client.reputation` - Soulbound tokens

### Common Patterns

```python
# Safe operation wrapper
def safe_operation(operation):
    try:
        return {"success": True, "result": operation()}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Batch processing
def process_batch(items, operation, batch_size=10):
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        for item in batch:
            result = safe_operation(lambda: operation(item))
            results.append(result)
    return results
```

## Support

- **Documentation**: See `/docs/` folder for detailed guides
- **Examples**: Check `/examples/` folder for complete workflows  
- **Issues**: Report bugs and feature requests on GitHub
- **API Reference**: Each module has detailed API documentation
