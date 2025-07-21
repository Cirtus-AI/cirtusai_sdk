# CirtusAI SDK Wallet Management Guide

## Overview

The CirtusAI SDK provides comprehensive wallet management capabilities including crypto wallet operations, asset management, email integration, RWA (Real World Assets) support, DeFi yield strategies, and advanced features like gas sponsorship and agent wallets.

## Features

- **Multi-Chain Wallet Support**: Create and manage wallets across multiple blockchains
- **Asset Management**: Track and manage crypto assets and email accounts
- **Transaction Management**: Send transactions, check balances, and monitor activity
- **Gas Sponsorship**: Sponsor gas fees for improved user experience
- **Onramp Integration**: Fiat-to-crypto conversion support
- **RWA Asset Registry**: Register and manage real-world assets
- **DeFi Yield Strategies**: Automated yield farming and strategy execution
- **Event Subscriptions**: Real-time blockchain event monitoring
- **Agent Wallets**: Smart contract wallets with programmable controls
- **Account Abstraction**: ERC-4337 user operations support

## Basic Wallet Operations

### Create and Manage Wallets

```python
from cirtusai import CirtusAIClient

client = CirtusAIClient("https://api.cirtusai.com")
client.set_token("your_access_token")

# Create a new wallet
wallet = client.wallets.create_wallet(chain="ethereum")
print(f"New wallet address: {wallet['address']}")
print(f"Chain: {wallet['chain']}")

# Import existing wallet
imported_wallet = client.wallets.import_wallet(
    chain="ethereum",
    private_key="your_private_key_hex"
)

# List all wallets
wallets = client.wallets.list_wallets()
for wallet in wallets:
    print(f"Wallet ID: {wallet['id']}")
    print(f"Address: {wallet['address']}")
    print(f"Chain: {wallet['chain']}")

# Delete wallet
client.wallets.delete_wallet("wallet_id")
```

### Asset Management

```python
# List all assets
assets = client.wallets.list_assets()
print(f"Total assets: {len(assets)}")

# Add individual asset
client.wallets.add_asset(
    asset_key="BTC_ADDRESS",
    asset_value="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
)

# Bulk add assets
assets_dict = {
    "ETH_ADDRESS": "0x742d35Cc6635C0532925a3b8D",
    "USDC_ADDRESS": "0xA0b86a33E6c3b",
    "API_KEY": "your_api_key_here"
}
client.wallets.bulk_add_assets(assets_dict)

# Add crypto wallet to assets
crypto_asset = client.wallets.add_crypto(chain="ethereum")
print(f"Crypto wallet added: {crypto_asset}")
```

## Transaction Operations

### Token Operations

```python
# Get token balance
balance = client.wallets.get_token_balance(
    wallet_id="wallet_123",
    token_address="0xA0b86a33E6c3b"  # USDC
)
print(f"Token balance: {balance}")

# Transfer tokens
transfer_result = client.wallets.transfer_tokens(
    wallet_id="wallet_123",
    token_address="0xA0b86a33E6c3b",
    to_address="0x742d35Cc6635C0532925a3b8D",
    amount=100.0
)
print(f"Transfer hash: {transfer_result['transaction_hash']}")

# Approve token spending
approval_result = client.wallets.approve_tokens(
    wallet_id="wallet_123",
    token_address="0xA0b86a33E6c3b",
    spender_address="0x1234567890123456789012345678901234567890",
    amount=1000.0
)
```

### Native Currency Operations

```python
# Get native balance (ETH, MATIC, etc.)
balance = client.wallets.get_balance(
    chain="ethereum",
    address="0x742d35Cc6635C0532925a3b8D"
)
print(f"ETH balance: {balance}")

# Send raw transaction
tx_hash = client.wallets.send_transaction(
    chain="ethereum",
    to="0x742d35Cc6635C0532925a3b8D",
    signed_tx="0x1234567890abcdef"  # Pre-signed transaction
)
print(f"Transaction hash: {tx_hash}")
```

## Gas Management

### Gas Sponsorship

```python
# Sponsor gas for token transactions
sponsorship_hash = client.wallets.sponsor_gas(
    token_address="0xA0b86a33E6c3b",
    amount=Decimal("100.0")
)
print(f"Gas sponsorship transaction: {sponsorship_hash}")

# Check gas sponsorship balance
sponsorship_balance = client.wallets.get_gas_sponsorship_balance()
print(f"Available gas sponsorship: {sponsorship_balance}")
```

## Fiat Onramp Integration

### Create Onramp Session

```python
# Create fiat-to-crypto onramp session
onramp_session = client.wallets.create_onramp_session(
    currency="USD",
    amount=500.0
)

print(f"Session ID: {onramp_session['session_id']}")
print(f"Payment URL: {onramp_session['payment_url']}")
print(f"Status: {onramp_session['status']}")

# Check onramp status
status = client.wallets.get_onramp_status(onramp_session['session_id'])
print(f"Onramp status: {status['status']}")
print(f"Amount received: {status.get('amount_received', 0)}")
```

## Real World Assets (RWA)

### RWA Asset Management

```python
# Register RWA asset
rwa_asset = client.wallets.register_rwa_asset(
    token_address="0x1234567890123456789012345678901234567890",
    token_id="123",
    metadata_uri="https://metadata.example.com/asset/123"
)

print(f"RWA Asset registered: {rwa_asset['asset_id']}")
print(f"Status: {rwa_asset['status']}")

# List all RWA assets
rwa_assets = client.wallets.list_rwa_assets()
for asset in rwa_assets:
    print(f"Asset ID: {asset['asset_id']}")
    print(f"Token Address: {asset['token_address']}")
    print(f"Token ID: {asset['token_id']}")

# Transfer RWA asset
transfer_hash = client.wallets.transfer_rwa_asset(
    asset_id="rwa_asset_123",
    to_address="0x742d35Cc6635C0532925a3b8D"
)
print(f"RWA transfer hash: {transfer_hash}")
```

## DeFi Yield Strategies

### Yield Strategy Management

```python
# Create yield strategy
strategy = client.wallets.create_yield_strategy(
    asset_key="USDC_BALANCE",
    protocol="aave",
    min_apr=Decimal("5.0")  # 5% minimum APR
)

print(f"Strategy ID: {strategy['strategy_id']}")
print(f"Protocol: {strategy['protocol']}")
print(f"Target APR: {strategy['target_apr']}")

# List all yield strategies
strategies = client.wallets.list_yield_strategies()
for strategy in strategies:
    print(f"Strategy: {strategy['strategy_id']}")
    print(f"Asset: {strategy['asset_key']}")
    print(f"Current APR: {strategy['current_apr']}")

# Execute yield strategy
execution_result = client.wallets.run_yield_strategy("strategy_123")
print(f"Execution status: {execution_result['status']}")
print(f"Amount deployed: {execution_result['amount_deployed']}")
```

## Event Monitoring

### Blockchain Event Subscriptions

```python
# Subscribe to blockchain events
subscription_id = client.wallets.subscribe_event(
    chain="ethereum",
    filter_criteria={
        "address": "0x1234567890123456789012345678901234567890",
        "topics": ["Transfer(address,address,uint256)"]
    },
    callback_url="https://your-webhook.com/events"
)

print(f"Subscription ID: {subscription_id}")

# List active subscriptions
subscriptions = client.wallets.list_event_subscriptions()
for sub in subscriptions:
    print(f"Subscription: {sub['subscription_id']}")
    print(f"Chain: {sub['chain']}")
    print(f"Status: {sub['status']}")

# Unsubscribe from events
client.wallets.unsubscribe_event(subscription_id)
```

## Agent Wallets (Smart Contract Wallets)

### Deploy and Manage Agent Wallets

```python
# Deploy new agent wallet
agent_wallet = client.wallets.deploy_agent_wallet()
print(f"Agent wallet address: {agent_wallet['address']}")
print(f"Deployment hash: {agent_wallet['deployment_hash']}")

# List all agent wallets
agent_wallets = client.wallets.list_agent_wallets()
for wallet in agent_wallets:
    print(f"Address: {wallet['address']}")
    print(f"Owner: {wallet['owner']}")
    print(f"Threshold: {wallet['threshold']}")

# Get specific agent wallet details
wallet_details = client.wallets.get_agent_wallet("0x1234567890123456789012345678901234567890")
print(f"Spending limits: {wallet_details['spending_limits']}")
print(f"Whitelist: {wallet_details['whitelist']}")
```

### Agent Wallet Configuration

```python
# Set spending limits
limit_hash = client.wallets.set_spending_limit(
    address="0x1234567890123456789012345678901234567890",
    token="0xA0b86a33E6c3b",  # USDC
    amount=1000,  # 1000 USDC
    period=86400  # 24 hours
)

# Update whitelist
whitelist_hash = client.wallets.update_whitelist(
    address="0x1234567890123456789012345678901234567890",
    target="0x742d35Cc6635C0532925a3b8D",
    allowed=True
)

# Set multi-sig threshold
threshold_hash = client.wallets.set_threshold(
    address="0x1234567890123456789012345678901234567890",
    new_threshold=2  # Require 2 signatures
)
```

### Agent Wallet Transactions

```python
# List wallet transactions
transactions = client.wallets.list_wallet_transactions(
    address="0x1234567890123456789012345678901234567890"
)

for tx in transactions:
    print(f"Hash: {tx['hash']}")
    print(f"To: {tx['to']}")
    print(f"Value: {tx['value']}")
    print(f"Status: {tx['status']}")
```

## Account Abstraction (ERC-4337)

### User Operations

```python
# Send user operation
user_op = {
    "sender": "0x1234567890123456789012345678901234567890",
    "nonce": "0x1",
    "initCode": "0x",
    "callData": "0xa9059cbb000000000000000000000000742d35cc6635c0532925a3b8d00000000000000000000000000000000000000000000000000000000000000064",
    "callGasLimit": "0x5208",
    "verificationGasLimit": "0x186a0",
    "preVerificationGas": "0x5208",
    "maxFeePerGas": "0x77359400",
    "maxPriorityFeePerGas": "0x77359400",
    "paymasterAndData": "0x",
    "signature": "0x..."
}

result = client.wallets.send_user_operation(
    user_op=user_op,
    entry_point_address="0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789"
)

print(f"User operation hash: {result['userOpHash']}")

# Check user operation status
status = client.wallets.get_user_operation_status(result['userOpHash'])
print(f"Status: {status['status']}")
print(f"Transaction hash: {status.get('transactionHash')}")
```

## Email Integration

### Email Account Management

```python
# List email accounts
email_accounts = client.wallets.list_email_accounts()
for account in email_accounts:
    print(f"Account ID: {account['id']}")
    print(f"Email: {account['email_address']}")
    print(f"Provider: {account['provider']}")

# Create email account
email_account = client.wallets.create_email_account(
    provider="gmail",
    email_address="user@gmail.com",
    config={
        "refresh_token": "your_refresh_token",
        "client_id": "your_client_id",
        "client_secret": "your_client_secret"
    }
)

# Get specific email account
account = client.wallets.get_email_account("account_123")
print(f"Email: {account['email_address']}")
print(f"Status: {account['status']}")

# Update email account
updated_account = client.wallets.update_email_account(
    account_id="account_123",
    provider="gmail",
    email_address="updated@gmail.com",
    config={"refresh_token": "new_refresh_token"}
)

# Refresh email token
refreshed = client.wallets.refresh_email_token("account_123")
print(f"Token refreshed: {refreshed['success']}")

# Delete email account
client.wallets.delete_email_account("account_123")
```

## Advanced Wallet Workflows

### Multi-Chain Portfolio Management

```python
def manage_multi_chain_portfolio(client):
    """Manage assets across multiple chains"""
    
    # Create wallets on different chains
    chains = ["ethereum", "polygon", "arbitrum"]
    wallets = {}
    
    for chain in chains:
        wallet = client.wallets.create_wallet(chain=chain)
        wallets[chain] = wallet
        print(f"Created {chain} wallet: {wallet['address']}")
    
    # Check balances across all chains
    portfolio = {}
    for chain, wallet in wallets.items():
        try:
            balance = client.wallets.get_balance(chain, wallet['address'])
            portfolio[chain] = balance
        except Exception as e:
            print(f"Error getting {chain} balance: {e}")
            portfolio[chain] = 0
    
    return portfolio

# Usage
portfolio = manage_multi_chain_portfolio(client)
print(f"Portfolio balances: {portfolio}")
```

### Automated Yield Farming

```python
def setup_yield_farming(client, asset_allocation):
    """Setup automated yield farming across protocols"""
    
    strategies = []
    
    for asset, config in asset_allocation.items():
        try:
            strategy = client.wallets.create_yield_strategy(
                asset_key=asset,
                protocol=config["protocol"],
                min_apr=config["min_apr"]
            )
            strategies.append(strategy)
            
            # Execute strategy immediately if configured
            if config.get("auto_execute", False):
                result = client.wallets.run_yield_strategy(strategy['strategy_id'])
                print(f"Executed strategy {strategy['strategy_id']}: {result['status']}")
                
        except Exception as e:
            print(f"Failed to create strategy for {asset}: {e}")
    
    return strategies

# Usage
allocation = {
    "USDC_BALANCE": {
        "protocol": "aave",
        "min_apr": Decimal("4.0"),
        "auto_execute": True
    },
    "ETH_BALANCE": {
        "protocol": "compound",
        "min_apr": Decimal("3.5"),
        "auto_execute": False
    }
}

strategies = setup_yield_farming(client, allocation)
```

### Smart Contract Interaction

```python
def deploy_and_configure_agent_wallet(client, config):
    """Deploy and fully configure an agent wallet"""
    
    # Deploy agent wallet
    wallet = client.wallets.deploy_agent_wallet()
    address = wallet['address']
    
    print(f"Deployed agent wallet: {address}")
    
    # Configure spending limits
    for token, limit_config in config['spending_limits'].items():
        client.wallets.set_spending_limit(
            address=address,
            token=token,
            amount=limit_config['amount'],
            period=limit_config['period']
        )
    
    # Setup whitelist
    for target in config['whitelist']:
        client.wallets.update_whitelist(
            address=address,
            target=target,
            allowed=True
        )
    
    # Set multi-sig threshold
    if config.get('threshold'):
        client.wallets.set_threshold(address, config['threshold'])
    
    return wallet

# Usage
wallet_config = {
    "spending_limits": {
        "0xA0b86a33E6c3b": {"amount": 1000, "period": 86400},  # USDC daily limit
        "0x0000000000000000000000000000000000000000": {"amount": 1, "period": 86400}  # ETH daily limit
    },
    "whitelist": [
        "0x742d35Cc6635C0532925a3b8D",
        "0x1234567890123456789012345678901234567890"
    ],
    "threshold": 2
}

agent_wallet = deploy_and_configure_agent_wallet(client, wallet_config)
```

## Error Handling and Best Practices

### Transaction Safety

```python
def safe_token_transfer(client, wallet_id, token_address, to_address, amount):
    """Safely execute token transfer with checks"""
    
    try:
        # Check balance first
        balance = client.wallets.get_token_balance(wallet_id, token_address)
        
        if balance['balance'] < amount:
            return {"success": False, "error": "Insufficient balance"}
        
        # Execute transfer
        result = client.wallets.transfer_tokens(
            wallet_id=wallet_id,
            token_address=token_address,
            to_address=to_address,
            amount=amount
        )
        
        return {"success": True, "transaction_hash": result['transaction_hash']}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# Usage
result = safe_token_transfer(
    client, "wallet_123", "0xA0b86a33E6c3b", 
    "0x742d35Cc6635C0532925a3b8D", 100.0
)

if result["success"]:
    print(f"Transfer successful: {result['transaction_hash']}")
else:
    print(f"Transfer failed: {result['error']}")
```

### Gas Optimization

```python
def optimize_gas_usage(client, operations):
    """Optimize gas usage for multiple operations"""
    
    # Check gas sponsorship balance
    sponsorship_balance = client.wallets.get_gas_sponsorship_balance()
    
    if sponsorship_balance > 0:
        print(f"Using gas sponsorship: {sponsorship_balance} available")
        
        # Execute operations using sponsored gas
        for op in operations:
            try:
                if op['type'] == 'transfer':
                    result = client.wallets.transfer_tokens(**op['params'])
                    print(f"Sponsored transfer: {result['transaction_hash']}")
            except Exception as e:
                print(f"Operation failed: {e}")
    else:
        print("No gas sponsorship available, using regular gas")
        # Execute operations normally

# Usage
operations = [
    {
        "type": "transfer",
        "params": {
            "wallet_id": "wallet_123",
            "token_address": "0xA0b86a33E6c3b",
            "to_address": "0x742d35Cc6635C0532925a3b8D",
            "amount": 50.0
        }
    }
]

optimize_gas_usage(client, operations)
```

## API Reference

### WalletsClient Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `create_wallet()` | Create new wallet | chain | Dict |
| `import_wallet()` | Import existing wallet | chain, private_key | Dict |
| `list_wallets()` | List all wallets | - | List[Dict] |
| `delete_wallet()` | Delete wallet | wallet_id | None |
| `get_token_balance()` | Get token balance | wallet_id, token_address | Dict |
| `transfer_tokens()` | Transfer tokens | wallet_id, token_address, to_address, amount | Dict |
| `approve_tokens()` | Approve token spending | wallet_id, token_address, spender_address, amount | Dict |
| `get_balance()` | Get native currency balance | chain, address | Decimal |
| `send_transaction()` | Send raw transaction | chain, to, signed_tx | str |
| `sponsor_gas()` | Sponsor gas fees | token_address, amount | str |
| `get_gas_sponsorship_balance()` | Get sponsorship balance | - | Decimal |
| `create_onramp_session()` | Create fiat onramp | currency, amount | Dict |
| `get_onramp_status()` | Check onramp status | session_id | Dict |
| `register_rwa_asset()` | Register RWA asset | token_address, token_id, metadata_uri | Dict |
| `list_rwa_assets()` | List RWA assets | - | List[Dict] |
| `transfer_rwa_asset()` | Transfer RWA asset | asset_id, to_address | str |
| `create_yield_strategy()` | Create yield strategy | asset_key, protocol, min_apr | Dict |
| `list_yield_strategies()` | List yield strategies | - | List[Dict] |
| `run_yield_strategy()` | Execute yield strategy | strategy_id | Dict |
| `subscribe_event()` | Subscribe to events | chain, filter_criteria, callback_url | str |
| `list_event_subscriptions()` | List subscriptions | - | List[Dict] |
| `unsubscribe_event()` | Unsubscribe from events | subscription_id | None |
| `deploy_agent_wallet()` | Deploy agent wallet | - | Dict |
| `list_agent_wallets()` | List agent wallets | - | List[Dict] |
| `get_agent_wallet()` | Get agent wallet details | address | Dict |
| `set_spending_limit()` | Set spending limit | address, token, amount, period | str |
| `update_whitelist()` | Update whitelist | address, target, allowed | str |
| `set_threshold()` | Set multi-sig threshold | address, new_threshold | str |
| `list_wallet_transactions()` | List wallet transactions | address | List[Dict] |
| `send_user_operation()` | Send user operation | user_op, entry_point_address | Dict |
| `get_user_operation_status()` | Get user op status | user_op_hash | Dict |
