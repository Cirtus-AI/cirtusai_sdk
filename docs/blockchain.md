# CirtusAI SDK Blockchain Infrastructure Guide

## Overview

The CirtusAI SDK provides comprehensive blockchain infrastructure components including cross-chain bridging, DeFi swaps, NFT management, governance operations, identity management, and marketplace functionality. These modules enable seamless interaction with multiple blockchain networks.

## Cross-Chain Bridge

### Bridge Operations

```python
from cirtusai import CirtusAIClient

client = CirtusAIClient("https://api.cirtusai.com")
client.set_token("your_access_token")

# Get bridge quote for cross-chain transfer
quote = client.bridge.get_quote(
    from_chain="ethereum",
    to_chain="polygon",
    from_token="ETH",
    to_token="MATIC",
    amount=1000000000000000000  # 1 ETH in wei
)

print(f"Estimated output: {quote['estimated_output']}")
print(f"Fee: {quote['fee']}")
print(f"Estimated time: {quote['estimated_time']}")

# Execute bridge transfer
bridge_result = client.bridge.bridge_transfer(
    provider="multichain",
    from_chain="ethereum",
    to_chain="polygon", 
    from_token="ETH",
    to_token="MATIC",
    amount=1000000000000000000,
    recipient_address="0x742d35Cc6635C0532925a3b8D"
)

print(f"Bridge transaction: {bridge_result['transaction_hash']}")
print(f"Bridge ID: {bridge_result['bridge_id']}")
```

### Multi-Chain Asset View

```python
# Get consolidated view of assets across chains
asset_view = client.bridge.get_multi_chain_asset_view()

print("Multi-chain asset portfolio:")
for chain, assets in asset_view.items():
    print(f"\n{chain.upper()}:")
    for asset in assets:
        print(f"  {asset['symbol']}: {asset['balance']} ({asset['usd_value']} USD)")

# Refresh the asset view
refreshed_view = client.bridge.refresh_multi_chain_asset_view()
print(f"Asset view refreshed: {refreshed_view['updated_at']}")
```

## DeFi Swap Operations

### Token Swaps

```python
# Get swap quote
swap_quote = client.swap.get_quote(
    from_chain="ethereum",
    to_chain="ethereum",
    from_token="USDC",
    to_token="ETH",
    amount=1000.0  # 1000 USDC
)

print(f"Estimated ETH output: {swap_quote['estimated_output']}")
print(f"Price impact: {swap_quote['price_impact']}%")
print(f"Slippage tolerance: {swap_quote['slippage_tolerance']}%")

# Execute swap
swap_data = {
    "from_token": "USDC",
    "to_token": "ETH",
    "amount": 1000.0,
    "slippage_tolerance": 0.5,
    "deadline": 1800  # 30 minutes
}

swap_result = client.swap.execute_swap(swap_data)
print(f"Swap transaction: {swap_result['transaction_hash']}")
print(f"Swap ID: {swap_result['swap_id']}")

# Cancel pending swap if needed
client.swap.cancel_swap("swap_123")
```

## NFT Management

### NFT Operations

```python
# List NFTs in wallet
nfts = client.nfts.list_nfts(wallet_id="wallet_123")
for nft in nfts:
    print(f"Contract: {nft['contract_address']}")
    print(f"Token ID: {nft['token_id']}")
    print(f"Name: {nft['name']}")
    print(f"Description: {nft['description']}")

# Get specific NFT metadata
metadata = client.nfts.get_nft_metadata(
    contract_address="0x1234567890123456789012345678901234567890",
    token_id="1"
)
print(f"NFT metadata: {metadata}")

# Mint new NFT
mint_result = client.nfts.mint_nft(
    contract_address="0x1234567890123456789012345678901234567890",
    to_address="0x742d35Cc6635C0532925a3b8D",
    metadata_uri="https://metadata.example.com/nft/1"
)
print(f"Mint transaction: {mint_result['transaction_hash']}")

# Batch transfer NFTs
transfers = [
    {
        "token_id": "1",
        "to_address": "0x742d35Cc6635C0532925a3b8D"
    },
    {
        "token_id": "2", 
        "to_address": "0x1234567890123456789012345678901234567890"
    }
]

batch_result = client.nfts.batch_transfer(
    contract_address="0x1234567890123456789012345678901234567890",
    transfers=transfers
)

# Burn NFT
client.nfts.burn_nft(
    contract_address="0x1234567890123456789012345678901234567890",
    token_id="3"
)
```

## Governance

### DAO Governance Operations

```python
# Create governance proposal
proposal = client.governance.create_proposal(
    targets=["0x1234567890123456789012345678901234567890"],
    values=[0],
    calldatas=["0xa9059cbb000000000000000000000000742d35cc6635c0532925a3b8d00000000000000000000000000000000000000000000000000000000000000064"],
    description="Transfer 100 tokens to community fund"
)

print(f"Proposal ID: {proposal['proposal_id']}")
print(f"Proposal state: {proposal['state']}")

# Cast vote on proposal
vote_result = client.governance.cast_vote(
    proposal_id=1,
    support=1  # 0=against, 1=for, 2=abstain
)
print(f"Vote transaction: {vote_result['transaction_hash']}")

# Get proposal state
proposal_state = client.governance.get_proposal_state(proposal_id=1)
print(f"Current state: {proposal_state['state']}")
print(f"For votes: {proposal_state['for_votes']}")
print(f"Against votes: {proposal_state['against_votes']}")
```

## Identity & Reputation

### Decentralized Identity (DID)

```python
# Get DID for agent
did_info = client.identity.get_did(agent_id="agent_123")
print(f"DID: {did_info['did']}")
print(f"Public key: {did_info['public_key']}")

# Issue verifiable credential
credential = client.identity.issue_credential(
    subject_id="user_123",
    types=["VerifiableCredential", "KYCCredential"],
    claim={
        "kyc_verified": True,
        "verification_level": "enhanced",
        "verified_at": "2024-01-15T10:30:00Z"
    }
)
print(f"Credential issued: {credential['credential_id']}")

# Verify credential
verification = client.identity.verify_credential(
    jwt_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
)
print(f"Verification status: {verification['valid']}")
print(f"Claims: {verification['claims']}")
```

### Soulbound Tokens (SBT)

```python
# Issue soulbound token for reputation
sbt_result = client.reputation.issue_sbt(
    to_address="0x742d35Cc6635C0532925a3b8D",
    token_uri="https://metadata.example.com/sbt/reputation/1"
)
print(f"SBT transaction: {sbt_result['transaction_hash']}")

# Get SBT owner
owner = client.reputation.get_sbt_owner(token_id=1)
print(f"SBT owner: {owner}")
```

## Marketplace

### NFT Marketplace Operations

```python
# Create marketplace listing
listing_data = {
    "nft_contract": "0x1234567890123456789012345678901234567890",
    "token_id": "1",
    "price": "1.5",  # ETH
    "currency": "ETH",
    "duration": 7  # days
}

listing = client.marketplace.create_listing(listing_data)
print(f"Listing ID: {listing['listing_id']}")
print(f"Status: {listing['status']}")

# Get specific listing
listing_info = client.marketplace.get_listing("listing_123")
print(f"Price: {listing_info['price']} {listing_info['currency']}")
print(f"Seller: {listing_info['seller']}")

# List all available listings
listings = client.marketplace.list_listings(
    filters={
        "min_price": 0.1,
        "max_price": 10.0,
        "currency": "ETH"
    }
)

for listing in listings:
    print(f"Listing {listing['listing_id']}: {listing['price']} {listing['currency']}")

# Place bid on listing
bid_data = {
    "price": "1.2",
    "currency": "ETH",
    "expires_at": "2024-01-20T10:30:00Z"
}

bid = client.marketplace.place_bid(
    listing_id="listing_123",
    bid_data=bid_data
)
print(f"Bid placed: {bid['bid_id']}")

# List bids for a listing
bids = client.marketplace.list_bids("listing_123")
for bid in bids:
    print(f"Bid {bid['bid_id']}: {bid['price']} {bid['currency']} by {bid['bidder']}")

# Accept bid (as seller)
accept_result = client.marketplace.accept_bid(
    listing_id="listing_123",
    bid_id="bid_456"
)
print(f"Bid accepted: {accept_result['transaction_hash']}")

# Update listing
updated_listing = client.marketplace.update_listing(
    listing_id="listing_123",
    listing_data={"price": "1.3"}
)

# Cancel listing
client.marketplace.cancel_listing("listing_123")
```

## Child Assets Management

### Child Agent Asset Operations

```python
# List assets for child agent
child_assets = client.child_assets.list_child_assets(child_id="child_123")
for asset in child_assets:
    print(f"Asset ID: {asset['asset_id']}")
    print(f"Type: {asset['asset_type']}")
    print(f"Value: {asset['asset_value']}")

# Get specific child asset
asset = client.child_assets.get_child_asset("asset_123")
print(f"Asset details: {asset}")

# Create new asset for child
asset_data = {
    "asset_type": "email_account",
    "asset_value": "child_agent@example.com",
    "metadata": {
        "provider": "gmail",
        "configured": True
    }
}

new_asset = client.child_assets.create_child_asset(
    child_id="child_123",
    asset_data=asset_data
)
print(f"Created asset: {new_asset['asset_id']}")

# Update child asset
updated_asset = client.child_assets.update_child_asset(
    asset_id="asset_123",
    asset_data={"metadata": {"status": "active"}}
)

# Delete child asset
client.child_assets.delete_child_asset("asset_123")
```

## Advanced Blockchain Workflows

### Cross-Chain DeFi Strategy

```python
def execute_cross_chain_strategy(client, strategy_config):
    """Execute complex cross-chain DeFi strategy"""
    
    results = []
    
    for step in strategy_config["steps"]:
        if step["type"] == "bridge":
            # Bridge assets to target chain
            quote = client.bridge.get_quote(
                from_chain=step["from_chain"],
                to_chain=step["to_chain"],
                from_token=step["from_token"],
                to_token=step["to_token"],
                amount=step["amount"]
            )
            
            if quote["estimated_output"] >= step["min_output"]:
                bridge_result = client.bridge.bridge_transfer(
                    provider=step["provider"],
                    from_chain=step["from_chain"],
                    to_chain=step["to_chain"],
                    from_token=step["from_token"],
                    to_token=step["to_token"],
                    amount=step["amount"],
                    recipient_address=step["recipient"]
                )
                results.append({"step": "bridge", "result": bridge_result})
        
        elif step["type"] == "swap":
            # Execute DeFi swap
            swap_result = client.swap.execute_swap(step["swap_data"])
            results.append({"step": "swap", "result": swap_result})
    
    return results

# Strategy configuration
strategy = {
    "steps": [
        {
            "type": "bridge",
            "from_chain": "ethereum",
            "to_chain": "polygon",
            "from_token": "USDC",
            "to_token": "USDC",
            "amount": 1000,
            "min_output": 995,
            "provider": "multichain",
            "recipient": "0x742d35Cc6635C0532925a3b8D"
        },
        {
            "type": "swap",
            "swap_data": {
                "from_token": "USDC",
                "to_token": "MATIC",
                "amount": 1000,
                "slippage_tolerance": 0.5
            }
        }
    ]
}

results = execute_cross_chain_strategy(client, strategy)
print(f"Strategy executed with {len(results)} steps")
```

### NFT Collection Management

```python
def manage_nft_collection(client, collection_config):
    """Comprehensive NFT collection management"""
    
    collection_stats = {
        "total_nfts": 0,
        "minted": 0,
        "transferred": 0,
        "listed": 0
    }
    
    # Mint NFTs in batch
    for i in range(collection_config["mint_count"]):
        try:
            mint_result = client.nfts.mint_nft(
                contract_address=collection_config["contract"],
                to_address=collection_config["owner"],
                metadata_uri=f"{collection_config['base_uri']}/{i}"
            )
            collection_stats["minted"] += 1
            print(f"Minted NFT #{i}: {mint_result['transaction_hash']}")
        except Exception as e:
            print(f"Failed to mint NFT #{i}: {e}")
    
    # List NFTs on marketplace
    nfts = client.nfts.list_nfts(collection_config["wallet_id"])
    
    for nft in nfts[:collection_config.get("list_count", 5)]:
        try:
            listing_data = {
                "nft_contract": nft["contract_address"],
                "token_id": nft["token_id"],
                "price": collection_config["list_price"],
                "currency": "ETH",
                "duration": 30
            }
            
            listing = client.marketplace.create_listing(listing_data)
            collection_stats["listed"] += 1
            print(f"Listed NFT {nft['token_id']}: {listing['listing_id']}")
        except Exception as e:
            print(f"Failed to list NFT {nft['token_id']}: {e}")
    
    return collection_stats

# Collection configuration
config = {
    "contract": "0x1234567890123456789012345678901234567890",
    "owner": "0x742d35Cc6635C0532925a3b8D",
    "wallet_id": "wallet_123",
    "base_uri": "https://metadata.example.com/collection",
    "mint_count": 10,
    "list_count": 5,
    "list_price": "0.1"
}

stats = manage_nft_collection(client, config)
print(f"Collection stats: {stats}")
```

### DAO Governance Automation

```python
def automated_governance_participation(client, governance_config):
    """Automate DAO governance participation"""
    
    # Get current proposal state
    proposal_id = governance_config["proposal_id"]
    proposal_state = client.governance.get_proposal_state(proposal_id)
    
    print(f"Proposal {proposal_id} state: {proposal_state['state']}")
    
    # Voting logic based on configuration
    if proposal_state["state"] == "Active":
        voting_decision = governance_config.get("auto_vote")
        
        if voting_decision is not None:
            vote_result = client.governance.cast_vote(
                proposal_id=proposal_id,
                support=voting_decision
            )
            print(f"Automatic vote cast: {vote_result['transaction_hash']}")
        else:
            print("Manual voting required - no auto-vote configured")
    
    # Create new proposal if configured
    if governance_config.get("create_proposal"):
        proposal_data = governance_config["proposal_data"]
        new_proposal = client.governance.create_proposal(
            targets=proposal_data["targets"],
            values=proposal_data["values"],
            calldatas=proposal_data["calldatas"],
            description=proposal_data["description"]
        )
        print(f"New proposal created: {new_proposal['proposal_id']}")
    
    return {
        "current_proposal_state": proposal_state,
        "actions_taken": ["vote_cast"] if voting_decision is not None else []
    }

# Governance configuration
gov_config = {
    "proposal_id": 1,
    "auto_vote": 1,  # 1 = for, 0 = against, 2 = abstain
    "create_proposal": False,
    "proposal_data": {
        "targets": ["0x1234567890123456789012345678901234567890"],
        "values": [0],
        "calldatas": ["0x"],
        "description": "Community treasury allocation"
    }
}

governance_result = automated_governance_participation(client, gov_config)
```

## Error Handling

### Blockchain Operation Safety

```python
def safe_blockchain_operation(client, module, operation, *args, **kwargs):
    """Safely execute blockchain operations with proper error handling"""
    
    try:
        module_client = getattr(client, module)
        result = getattr(module_client, operation)(*args, **kwargs)
        return {"success": True, "result": result}
    
    except requests.exceptions.HTTPError as e:
        error_code = e.response.status_code
        
        if error_code == 400:
            return {"success": False, "error": "Invalid parameters"}
        elif error_code == 403:
            return {"success": False, "error": "Insufficient permissions"}
        elif error_code == 429:
            return {"success": False, "error": "Rate limit exceeded"}
        else:
            return {"success": False, "error": f"HTTP {error_code}: {e}"}
    
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

# Usage examples
bridge_result = safe_blockchain_operation(
    client, "bridge", "get_quote",
    "ethereum", "polygon", "ETH", "MATIC", 1000000000000000000
)

if bridge_result["success"]:
    print(f"Bridge quote: {bridge_result['result']}")
else:
    print(f"Bridge operation failed: {bridge_result['error']}")
```

## API Reference Summary

### Available Modules

| Module | Description | Key Methods |
|--------|-------------|-------------|
| `bridge` | Cross-chain bridging | `get_quote()`, `bridge_transfer()`, `get_multi_chain_asset_view()` |
| `swap` | DeFi token swaps | `get_quote()`, `execute_swap()`, `cancel_swap()` |
| `nfts` | NFT management | `list_nfts()`, `mint_nft()`, `batch_transfer()`, `burn_nft()` |
| `governance` | DAO governance | `create_proposal()`, `cast_vote()`, `get_proposal_state()` |
| `identity` | Decentralized identity | `get_did()`, `issue_credential()`, `verify_credential()` |
| `reputation` | Soulbound tokens | `issue_sbt()`, `get_sbt_owner()` |
| `marketplace` | NFT marketplace | `create_listing()`, `place_bid()`, `accept_bid()` |
| `child_assets` | Child agent assets | `list_child_assets()`, `create_child_asset()` |

### Common Response Patterns

All blockchain operations return transaction hashes and operation IDs for tracking:

```python
{
    "transaction_hash": "0x1234567890abcdef...",
    "operation_id": "op_123",
    "status": "pending" | "confirmed" | "failed",
    "block_number": 12345678,
    "gas_used": 21000
}
```
