# CirtusAI Python SDK - Complete Developer Guide (Updated July 2025)

🚀 **The Most Comprehensive SDK for Autonomous AI Agent Management with Blockchain-Level Security**

The CirtusAI Python SDK provides everything developers need to build powerful, secure, and compliant AI agent applications. From basic wallet management to advanced smart contract automation, from governance participation to real-world asset tokenization - this SDK unlocks the complete power of the CirtusAI platform.

## 🎯 What Makes CirtusAI Unique

- **🔐 Enterprise-Grade 2FA Security**: Mandatory TOTP authentication with time-sync tolerance
- **🤖 Smart Contract Agent Wallets**: On-chain spending limits, whitelists, and automated rule enforcement  
- **🌐 Multi-Chain Support**: Ethereum, Polygon, Arbitrum, and more
- **📧 Email Integration**: IMAP/SMTP and OAuth for seamless communication
- **🏛️ DAO Governance**: Participate in on-chain voting and proposal management
- **💱 DeFi Integration**: Swaps, yield farming, cross-chain bridges, and gas abstraction
- **🏠 Real-World Assets (RWA)**: Tokenize and manage physical assets on-chain
- **📊 Compliance Built-In**: KYC/AML, audit trails, and regulatory reporting
- **⚡ Production Ready**: Sync/async support, comprehensive error handling, and extensive testing

---

## 📦 Installation

```bash
# Install the latest stable SDK
pip install cirtusai-sdk

# Install the beta/pre-release version
pip install --pre cirtusai-sdk
```

---

## 🚀 Quick Start Guide

### 1. Authentication with 2FA (Required)

Every CirtusAI application starts with secure authentication:

```python
from cirtusai import CirtusAIClient
from cirtusai.auth import TwoFactorAuthenticationError

# Initialize the client
client = CirtusAIClient(base_url="http://localhost:8000")

# Register a new user (automatic 2FA setup)
setup_info = client.auth.register(
    username="mycompany_agent", 
    email="admin@mycompany.com",
    password="SuperSecure123!",
    preferred_2fa_method="totp"
)

# Save the QR code for your authenticator app
print(f"📱 Scan QR: data:image/png;base64,{setup_info.qr_code_image}")
print(f"🔑 Secret: {setup_info.secret}")
print(f"🔐 Backup codes: {setup_info.backup_codes}")

# Login with 2FA (one-step method)
try:
    token = client.auth.login_with_2fa(
        "mycompany_agent",
        "SuperSecure123!",
        "123456"  # Current TOTP code from authenticator
    )
    client.set_token(token.access_token)
    print("✅ Authenticated successfully!")
except TwoFactorAuthenticationError as e:
    print(f"❌ 2FA failed: {e}")
```

### 2. Create Your First Wallet

```python
# Create a new HD wallet
wallet = client.wallets.create_wallet(chain="ethereum")
print(f"💰 New wallet: {wallet['wallet_address']}")

# Import an existing wallet
imported = client.wallets.import_wallet(
    chain="ethereum",
    private_key="0x1234567890abcdef..."  # Your private key
)
print(f"📥 Imported wallet: {imported['wallet_address']}")

# List all your wallets
wallets = client.wallets.list_wallets()
for w in wallets:
    print(f"  {w['name']}: {w['wallet_address']} ({w['chain']})")
```

### 3. Deploy Your First Agent Wallet

Agent wallets are smart contracts with programmable rules:

```python
# Deploy a smart contract agent wallet
agent_wallet = client.wallets.deploy_agent_wallet()
print(f"🤖 Agent wallet deployed: {agent_wallet['wallet_address']}")

# Set spending limits (daily ETH limit)
tx_hash = client.wallets.set_spending_limit(
    address=agent_wallet['wallet_address'],
    token="0x0",  # ETH
    amount=1000000000000000000,  # 1 ETH in wei
    period=86400  # 24 hours
)
print(f"⚡ Spending limit set: {tx_hash}")

# Add trusted addresses to whitelist
whitelist_tx = client.wallets.update_whitelist(
    address=agent_wallet['wallet_address'],
    target="0x742d35Cc6634C0532925a3b8D0715a99C7DCF",
    allowed=True
)
print(f"✅ Address whitelisted: {whitelist_tx}")
```

### 4. Manage Child Agents

```python
# List master agents
agents = client.agents.list_agents()
print(f"Master agents: {agents}")

# Create a child agent under a master agent
child = client.agents.create_child_agent("my_master_id", "assistant_bot")
print(f"Created child agent: {child['id']}")

# List all child agents
children = client.agents.get_children()
print(f"Child agents: {children}")
```

---

## 🏗️ Complete Feature Guide

## 1. 🔐 Advanced Authentication & Security

### 1.1 Complete 2FA Management

```python
# Check current 2FA status
status = client.auth.get_2fa_status()
print(f"2FA enabled: {status.is_2fa_enabled}")

# Setup 2FA for existing users
setup = client.auth.setup_2fa()
print(f"New secret: {setup.secret}")

# Get QR code as image bytes
qr_bytes = client.auth.get_qr_code()
with open("qr_code.png", "wb") as f:
    f.write(qr_bytes)

# Debug time synchronization issues
debug_info = client.auth.debug_2fa()
print("Valid codes right now:")
for step, code in debug_info["valid_codes"].items():
    print(f"  {step}: {code}")

# Disable 2FA (requires password + TOTP)
result = client.auth.disable_2fa(
    totp_code="123456",
    password="SuperSecure123!"
)
print(f"2FA disabled: {result['enabled']}")
```

### 1.2 Session Management

```python
# Get current user information  
user_info = client.auth.get_user_info()
print(f"User: {user_info['username']} ({user_info['email']})")

# Refresh expired tokens
new_token = client.auth.refresh(refresh_token="your_refresh_token")
client.set_token(new_token.access_token)

# Logout and clear session
client.auth.logout()
```

---

## 2. 💰 Comprehensive Wallet Management

### 2.1 Multi-Chain Wallet Operations

```python
# Create wallets on different chains
eth_wallet = client.wallets.create_wallet(chain="ethereum")
poly_wallet = client.wallets.create_wallet(chain="polygon") 
arb_wallet = client.wallets.create_wallet(chain="arbitrum")

# Get wallet balances
balance = client.wallets.get_balance(
    chain="ethereum",
    address=eth_wallet['wallet_address']
)
print(f"ETH Balance: {balance}")

# Get consolidated asset view across all chains
assets = client.assets.get_multi_chain_asset_view()
print(f"Total portfolio value: ${assets['total_value_usd']}")
for chain, data in assets['chains'].items():
    print(f"  {chain}: {data['native_balance']} native + {len(data['tokens'])} tokens")
```

### 2.2 ERC-20 Token Management

```python
# Get token balance
usdc_balance = client.wallets.get_token_balance(
    wallet_id=eth_wallet['id'],
    token_address="0xA0b86a33E6D1cc22c435370bA9e4240EE8D5fE5"  # USDC
)
print(f"USDC: {usdc_balance['balance']} {usdc_balance['symbol']}")

# Transfer tokens
transfer_tx = client.wallets.transfer_tokens(
    wallet_id=eth_wallet['id'],
    token_address="0xA0b86a33E6D1cc22c435370bA9e4240EE8D5fE5",
    to_address="0x742d35Cc6634C0532925a3b8D0715a99C7DCF",
    amount=100.0
)
print(f"Transfer completed: {transfer_tx['tx_hash']}")

# Approve token spending
approve_tx = client.wallets.approve_tokens(
    wallet_id=eth_wallet['id'], 
    token_address="0xA0b86a33E6D1cc22c435370bA9e4240EE8D5fE5",
    spender_address="0x1234567890abcdef...",
    amount=500.0
)
print(f"Approval set: {approve_tx['tx_hash']}")
```

---

## 3. 🤖 Agent Wallet Smart Contracts

### 3.1 Agent Wallet Deployment & Management

```python
# Deploy multiple agent wallets for different purposes
marketing_agent = client.wallets.deploy_agent_wallet()
finance_agent = client.wallets.deploy_agent_wallet()
ops_agent = client.wallets.deploy_agent_wallet()

# List all agent wallets
agent_wallets = client.wallets.list_agent_wallets()
for wallet in agent_wallets:
    print(f"Agent: {wallet['wallet_address']} (deployed: {wallet['created_at']})")

# Get detailed wallet information
wallet_details = client.wallets.get_agent_wallet(
    address=marketing_agent['wallet_address']
)
print(f"Wallet details: {wallet_details}")
```

### 3.2 On-Chain Rule Management

```python
# Set daily spending limits for different tokens
agent_addr = marketing_agent['wallet_address']

# ETH spending limit: 0.5 ETH per day
eth_limit = client.wallets.set_spending_limit(
    address=agent_addr,
    token="0x0",  # ETH
    amount=500000000000000000,  # 0.5 ETH in wei
    period=86400  # 24 hours
)

# USDC spending limit: $1000 per day  
usdc_limit = client.wallets.set_spending_limit(
    address=agent_addr,
    token="0xA0b86a33E6D1cc22c435370bA9e4240EE8D5fE5",  # USDC
    amount=1000000000,  # $1000 (6 decimals)
    period=86400
)

# Build a whitelist of approved addresses
approved_vendors = [
    "0x742d35Cc6634C0532925a3b8D0715a99C7DCF",  # OpenAI API payments
    "0x8b3a92Ef6F66F79A7B7C4D8f9E2A1B5C3D7E9F",   # AWS payments  
    "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a"    # Partner agent
]

for vendor in approved_vendors:
    whitelist_tx = client.wallets.update_whitelist(
        address=agent_addr,
        target=vendor,
        allowed=True
    )
    print(f"✅ Whitelisted {vendor}: {whitelist_tx}")

# Set transaction threshold requiring manual approval
threshold_tx = client.wallets.set_threshold(
    address=agent_addr,
    new_threshold=500  # Require approval for transactions > $500
)
print(f"🔒 Threshold set: {threshold_tx}")
```

### 3.3 Audit Trail & Event Monitoring

```python
# Get complete transaction history for an agent wallet
transactions = client.wallets.list_wallet_transactions(
    address=agent_addr
)

print(f"📊 Found {len(transactions)} events:")
for tx in transactions:
    print(f"  {tx['timestamp']}: {tx['event_name']}")
    print(f"    TX: {tx['tx_hash']}")
    print(f"    Details: {tx['details']}")
    print(f"    Block: {tx['block_number']}")
    print()

# Monitor for specific event types
spending_events = [tx for tx in transactions if tx['event_name'] == 'SpendingLimitSet']
whitelist_events = [tx for tx in transactions if tx['event_name'] == 'WhitelistUpdated']

print(f"🔍 Spending limit changes: {len(spending_events)}")
print(f"🔍 Whitelist updates: {len(whitelist_events)}")
```

---

## 4. 👥 Master/Child Agent Management

### 4.1 Agent Hierarchy Creation

```python
# Create a master agent for your organization
master_agent = client.agents.create_agent(
    name="Marketing Master Agent",
    description="Handles all marketing automation",
    agent_type="master",
    capabilities=["content_creation", "social_media", "email_marketing"]
)
print(f"👑 Master agent created: {master_agent['id']}")

# Create specialized child agents
social_media_agent = client.agents.create_agent(
    name="Social Media Specialist",
    description="Automated social media posting and engagement",
    agent_type="child",
    parent_id=master_agent['id'],
    capabilities=["social_media", "content_scheduling"]
)

email_agent = client.agents.create_agent(
    name="Email Campaign Manager", 
    description="Automated email marketing campaigns",
    agent_type="child",
    parent_id=master_agent['id'],
    capabilities=["email_marketing", "newsletter_automation"]
)

print(f"👶 Child agents created:")
print(f"  Social Media: {social_media_agent['id']}")
print(f"  Email: {email_agent['id']}")
```

### 4.2 Agent Rule Inheritance

```python
# Child agents inherit rules from their master
inherited_rules = client.agents.get_inherited_rules(
    child_id=social_media_agent['id']
)

print(f"📋 Inherited rules from master:")
print(f"  Spending limits: {inherited_rules['spending_limits']}")
print(f"  Whitelists: {inherited_rules['whitelists']}")
print(f"  Policies: {inherited_rules['policies']}")
```

### 4.3 Task Delegation

```python
# Delegate specific tasks to child agents
social_campaign = client.agents.delegate_task(
    master_id=master_agent['id'],
    child_agent_id=social_media_agent['id'],
    task_type="social_media_campaign",
    budget_allocation={
        "token": "0x0",  # ETH
        "amount": "50000000000000000"  # 0.05 ETH
    },
    deadline="2025-07-24T12:00:00Z",
    parameters={
        "platform": "twitter",
        "campaign_theme": "product_launch",
        "post_frequency": "3_per_day"
    }
)
print(f"📋 Task delegated: {social_campaign['id']}")

# Monitor delegation status
delegations = client.agents.list_delegations(master_agent['id'])
for delegation in delegations:
    print(f"Task: {delegation['task_type']} → {delegation['status']}")
```

---

## 5. 📧 Email Integration & Communication

### 5.1 Email Account Linking

```python
# Link IMAP/SMTP email account
email_account = client.wallets.create_email_account(
    provider="imap",
    email_address="marketing@mycompany.com",
    config={
        "host": "imap.gmail.com",
        "port": 993,
        "username": "marketing@mycompany.com", 
        "password": "app_password_here",  # Use app password for Gmail
        "use_ssl": True,
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587
    }
)
print(f"📧 Email account linked: {email_account['id']}")

# OAuth integration for Google/Outlook (redirect-based)
google_oauth_url = client.wallets.get_google_oauth_url()
print(f"🔗 Google OAuth: {google_oauth_url}")

# List all linked email accounts
email_accounts = client.wallets.list_email_accounts()
for account in email_accounts:
    print(f"  📬 {account['email_address']} ({account['provider']})")
```

### 5.2 Email Management & Access

```python
# Test email connection
test_result = client.wallets.test_email_connection(email_account['id'])
print(f"✅ Connection test: {test_result['status']}")

# Access inbox (with proper permissions)
inbox = client.wallets.get_inbox(
    account_id=email_account['id'],
    limit=10,
    unread_only=True
)
print(f"📨 Unread emails: {inbox['unread_count']}")
for msg in inbox['messages']:
    print(f"  From: {msg['from']}")
    print(f"  Subject: {msg['subject']}")
    print(f"  Date: {msg['date']}")
```

---

## 6. 🌉 Cross-Chain Bridge & DeFi

### 6.1 Cross-Chain Transfers

```python
# Get bridge quote for cross-chain transfer
quote = client.bridge.get_quote(
    from_chain="ethereum", 
    to_chain="polygon",
    from_token="0xA0b86a33E6D1cc22c435370bA9e4240EE8D5fE5",  # USDC
    to_token="0x2791bca1f2de4661ed88a30c99a7a9449aa84174",   # USDC on Polygon
    amount=1000000000  # $1000 USDC
)
print(f"💱 Bridge quote:")
print(f"  Fee: ${quote['fee_usd']}")
print(f"  Time: {quote['estimated_time']}")
print(f"  You'll receive: {quote['to_amount']} USDC on Polygon")

# Execute the bridge transfer
if quote['fee_usd'] < 10:  # Acceptable fee
    bridge_tx = client.bridge.bridge_transfer(
        provider=quote['provider'],
        from_chain="ethereum",
        to_chain="polygon", 
        from_token="0xA0b86a33E6D1cc22c435370bA9e4240EE8D5fE5",
        to_token="0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
        amount=1000000000,
        recipient_address=poly_wallet['wallet_address']
    )
    print(f"🌉 Bridge transfer initiated: {bridge_tx['tx_hash']}")
```

### 6.2 DeFi Integration

```python
# Swap tokens using integrated DEX
swap_tx = client.wallets.swap_tokens(
    wallet_id=eth_wallet['id'],
    from_token="0x0",  # ETH
    to_token="0xA0b86a33E6D1cc22c435370bA9e4240EE8D5fE5",  # USDC
    amount=1.0,  # 1 ETH
    slippage_tolerance=0.5  # 0.5%
)
print(f"🔄 Swap completed: {swap_tx['tx_hash']}")

# Deposit into yield farming vault
yield_deposit = client.wallets.deposit_yield_vault(
    wallet_id=eth_wallet['id'],
    vault_address="0x1234567890abcdef...",  # Aave USDC vault
    token_address="0xA0b86a33E6D1cc22c435370bA9e4240EE8D5fE5",
    amount=500.0
)
print(f"🌾 Yield farming deposit: {yield_deposit['tx_hash']}")

# Check yield farming positions
positions = client.wallets.get_yield_positions(eth_wallet['id'])
for position in positions:
    print(f"Vault: {position['vault_name']}")
    print(f"  Deposited: {position['deposited_amount']}")
    print(f"  Current value: {position['current_value']}")
    print(f"  APY: {position['apy']}%")
```

### 6.3 On-Chain Swap Services

```python
# Get swap quote for token pair
swap_quote = client.swap.get_quote(
    from_token="0x0",  # ETH
    to_token="0xA0b86a33E6D1cc22c435370bA9e4240EE8D5fE5",  # USDC
    amount=1.0
)
print(f"🔍 Swap quote: {swap_quote}")

# Execute the swap
swap_tx = client.swap.execute_swap(
    from_token="0x0",
    to_token="0xA0b86a33E6D1cc22c435370bA9e4240EE8D5fE5",
    amount=1.0,
    slippage_tolerance=0.5
)
print(f"🔄 Swap executed: {swap_tx['tx_hash']}")

# Cancel a pending swap quote
cancel = client.swap.cancel_swap(quote_id=swap_quote['quote_id'])
print(f"❌ Swap quote cancelled: {cancel['status']}")
```

### 6.4 Marketplace Operations

```python
# List marketplace listings
listings = client.marketplace.list_listings(limit=20)
for l in listings:
    print(f"Listing: {l['id']} - {l['asset_name']} at {l['price']}")

# Create a new listing
new_listing = client.marketplace.create_listing(
    asset_id="asset123",
    price="0.5 ETH",
    quantity=1
)
print(f"✅ Created listing: {new_listing['id']}")

# Place a bid on a listing
bid = client.marketplace.place_bid(
    listing_id=new_listing['id'],
    bid_amount="0.45 ETH"
)
print(f"🎯 Bid placed: {bid['bid_id']}")

# Cancel a listing
client.marketplace.cancel_listing(listing_id=new_listing['id'])
print("❌ Listing cancelled")
```

---

## 7. 🏛️ Governance & DAO Participation

### 7.1 Proposal Management

```python
# Create a governance proposal
proposal = client.governance.create_proposal(
    targets=["0x1234567890abcdef..."],  # Contract to call
    values=[0],  # ETH to send (0 for parameter change)
    calldatas=["0xabcdef..."],  # Encoded function call
    description="Increase agent spending limits to $2000/day"
)
print(f"📜 Proposal created: {proposal['proposal_id']}")

# Get proposal details
proposal_info = client.governance.get_proposal_state(proposal['proposal_id'])
print(f"Proposal status: {proposal_info['status']}")
print(f"Votes for: {proposal_info['votes_for']}")
print(f"Votes against: {proposal_info['votes_against']}")
print(f"Voting deadline: {proposal_info['voting_deadline']}")
```

### 7.2 Voting

```python
# Cast vote on proposal (1 = for, 0 = against)
vote = client.governance.cast_vote(
    proposal_id=proposal['proposal_id'],
    support=1  # Vote in favor
)
print(f"🗳️ Vote cast: {vote['tx_hash']}")

# Check your voting history
voting_history = client.governance.get_user_votes()
for vote_record in voting_history:
    print(f"Proposal {vote_record['proposal_id']}: {'FOR' if vote_record['support'] else 'AGAINST'}")
```

---

## 8. 🏠 Real-World Assets (RWA)

### 8.1 Asset Tokenization

```python
# Register a real-world asset token
rwa_asset = client.wallets.register_rwa_asset(
    token_address="0x9876543210fedcba...",  # RWA token contract
    token_id="1",  # Specific asset ID
    metadata_uri="https://metadata.example.com/asset/1"
)
print(f"🏠 RWA asset registered: {rwa_asset['id']}")

# List your RWA holdings
rwa_holdings = client.wallets.list_rwa_assets()
for asset in rwa_holdings:
    print(f"Asset: {asset['name']}")
    print(f"  Type: {asset['asset_type']}")
    print(f"  Value: ${asset['estimated_value']}")
    print(f"  Yield: {asset['annual_yield']}%")
```

### 8.2 Asset Management

```python
# Transfer RWA tokens
rwa_transfer = client.wallets.transfer_rwa(
    wallet_id=eth_wallet['id'],
    token_address="0x9876543210fedcba...",
    token_id="1",
    to_address="0x742d35Cc6634C0532925a3b8D0715a99C7DCF",
    amount=1
)
print(f"🔄 RWA transfer: {rwa_transfer['tx_hash']}")
```

---

## 9. 🎯 Child Asset Provisioning

### 9.1 Email Asset Provisioning

```python
# Provision email access to child agents
email_provision = client.agents.provision_email_asset(
    child_id=email_agent['id'],
    email_account_id=email_account['id'],
    permissions=["read", "send"],
    quota={
        "daily_emails": 100,
        "monthly_emails": 2000
    }
)
print(f"📧 Email access provisioned: {email_provision['email_address']}")

# Check email quota usage
email_usage = client.agents.get_email_usage(email_agent['id'])
print(f"Email usage: {email_usage['used_today']}/{email_usage['daily_limit']}")
```

### 9.2 Wallet Asset Provisioning

```python
# Provision dedicated wallets for child agents
child_eth_wallet = client.agents.provision_wallet_asset(
    child_id=social_media_agent['id'],
    chain="ethereum"
)
print(f"💰 Child wallet created: {child_eth_wallet['wallet_address']}")

child_poly_wallet = client.agents.provision_wallet_asset(
    child_id=social_media_agent['id'],
    chain="polygon"
)
print(f"💰 Child Polygon wallet: {child_poly_wallet['wallet_address']}")

# Transfer budget to child wallets
budget_transfer = client.agents.transfer_assets_to_child(
    child_id=social_media_agent['id'],
    from_wallet=eth_wallet['wallet_address'],
    to_wallet=child_eth_wallet['wallet_address'],
    asset_type="eth",
    amount="100000000000000000",  # 0.1 ETH
    note="Monthly social media budget"
)
print(f"💸 Budget transferred: {budget_transfer['transfer_id']}")
```

---

## 10. 💳 Fiat On/Off Ramps

### 10.1 Fiat Onboarding

```python
# Create fiat on-ramp session
onramp_session = client.wallets.create_onramp_session(
    currency="USD",
    amount=1000.0  # $1000
)
print(f"💳 On-ramp session: {onramp_session['session_id']}")
print(f"🔗 Widget URL: {onramp_session['widget_url']}")

# Check on-ramp status
onramp_status = client.wallets.get_onramp_status(
    session_id=onramp_session['session_id']
)
print(f"Status: {onramp_status['status']}")
if onramp_status['status'] == 'completed':
    print(f"✅ Received: {onramp_status['crypto_amount']} {onramp_status['crypto_currency']}")
```

---

## 11. ⛽ Gas Management & Abstraction

### 11.1 Gas Sponsorship

```python
# Deposit tokens for gas sponsorship
gas_deposit = client.wallets.sponsor_gas(
    token_address="0xA0b86a33E6D1cc22c435370bA9e4240EE8D5fE5",  # USDC
    amount=100.0  # $100 worth of gas
)
print(f"⛽ Gas sponsorship: {gas_deposit}")

# Check gas balance
gas_balance = client.wallets.get_gas_sponsorship_balance()
print(f"⛽ Gas balance: {gas_balance} USDC")

# Send gasless transaction using ERC-4337
user_op = client.wallets.send_user_operation(
    user_op={
        "sender": agent_addr,
        "nonce": "0x0",
        "initCode": "0x",
        "callData": "0x...",  # Your transaction data
        "callGasLimit": "0x5208",
        "verificationGasLimit": "0x5208", 
        "preVerificationGas": "0x5208",
        "maxFeePerGas": "0x3b9aca00",
        "maxPriorityFeePerGas": "0x3b9aca00",
        "paymasterAndData": "0x",
        "signature": "0x"
    },
    entry_point_address="0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789"
)
print(f"🚀 Gasless transaction: {user_op['user_op_hash']}")
```

---

## 12. 📊 Monitoring & Compliance

### 12.1 Transaction Monitoring

```python
# Start monitoring an address
monitoring = client.monitoring.watch_address(
    address="0x742d35Cc6634C0532925a3b8D0715a99C7DCF",
    alert_conditions=["large_transaction", "new_contract_interaction"]
)
print(f"👁️ Monitoring started: {monitoring['watch_id']}")

# Get transaction status
tx_status = client.monitoring.get_transaction_status(
    tx_hash="0xabcdef1234567890..."
)
print(f"Transaction status: {tx_status['status']}")
print(f"Confirmations: {tx_status['confirmations']}")

# List all active watches
watches = client.monitoring.list_watches()
for w in watches:
    print(f"👁️ Watch: {w['watch_id']} - {w['address']}")

# Retrieve recent alerts
alerts = client.monitoring.get_alerts()
for alert in alerts:
    print(f"⚠️ Alert: {alert['alert_id']} - {alert['type']} at {alert['timestamp']}")
```

### 12.2 Compliance & Reporting

```python
# Check KYC status
kyc_status = client.compliance.get_kyc_status()
print(f"KYC Status: {kyc_status['status']}")

# Initiate KYC if needed
if kyc_status['status'] == 'not_verified':
    kyc_session = client.compliance.initiate_kyc()
    print(f"🆔 KYC session: {kyc_session['verification_url']}")

# Generate compliance report
compliance_report = client.compliance.generate_report(
    start_date="2025-07-01",
    end_date="2025-07-17",
    report_type="full_audit"
)
print(f"📋 Compliance report:")
print(f"  Total transactions: {compliance_report['total_transactions']}")
print(f"  Total value: ${compliance_report['total_value_usd']}")
print(f"  Flagged activities: {compliance_report['flagged_count']}")
print(f"  Compliance score: {compliance_report['compliance_score']}/100")

# Get detailed audit trail for an entity
audit_trail = client.compliance.get_audit_trail(
    entity_id="entity123",
    entity_type="transaction"
)
print("📝 Audit trail entries:")
for entry in audit_trail:
    print(f"  {entry['timestamp']}: {entry['action']} by {entry['performed_by']}")
```

---

## 13. 🔥 Advanced Features

### 13.1 NFT Management

```python
# List NFTs in wallet
nfts = client.wallets.list_nfts(wallet_id=eth_wallet['id'])
for nft in nfts:
    print(f"🖼️ {nft['name']} #{nft['token_id']}")
    print(f"  Collection: {nft['collection_name']}")
    print(f"  Value: ${nft['estimated_value']}")

# Transfer NFT
nft_transfer = client.wallets.transfer_nft(
    wallet_id=eth_wallet['id'],
    contract_address="0x1234567890abcdef...",
    token_id="123", 
    to_address="0x742d35Cc6634C0532925a3b8D0715a99C7DCF"
)
print(f"🖼️ NFT transferred: {nft_transfer['tx_hash']}")

# Get metadata for a specific NFT
metadata = client.nfts.get_nft_metadata(
    contract_address="0x1234567890abcdef...",
    token_id="123"
)
print(f"NFT Metadata: {metadata}")

# Mint a new NFT
minted = client.nfts.mint_nft(
    contract_address="0xNFTContract...",
    to_address="0x742d35Cc6634C0532925a3b8D0715a99C7DCF",
    metadata_uri="https://metadata.example.com/nft/1"
)
print(f"🎨 NFT minted: {minted['token_id']}")

# Batch transfer multiple NFTs
batch = client.nfts.batch_transfer(
    contract_address="0x1234567890abcdef...",
    transfers=[
        {"token_id": "123", "to_address": "0xabc..."},
        {"token_id": "124", "to_address": "0xdef..."}
    ]
)
print("🔀 Batch transfer complete")

# Burn an NFT
burn = client.nfts.burn_nft(
    contract_address="0x1234567890abcdef...",
    token_id="123"
)
print(f"🔥 NFT burned: {burn['status']}")
```

### 13.2 Event Subscriptions

```python
# Subscribe to wallet events
subscription = client.wallets.subscribe_to_events(
    wallet_address=eth_wallet['wallet_address'],
    event_types=["transfer", "approval", "swap"]
)
print(f"📡 Event subscription: {subscription['subscription_id']}")

# Get recent events
events = client.wallets.get_wallet_events(
    wallet_address=eth_wallet['wallet_address'],
    limit=50
)
for event in events:
    print(f"⚡ {event['event_type']}: {event['details']}")
```

## 📚 Complete API Reference

### AuthClient

- `register(username, email, password, preferred_2fa_method="totp")` → `TwoFactorSetupResponse`
- `login(username, password)` → `Token | TwoFactorRequiredResponse`
- `login_with_2fa(username, password, totp_code)` → `Token`
- `verify_2fa(temporary_token, totp_code)` → `Token`
- `get_2fa_status()` → `TwoFactorStatusResponse`
- `setup_2fa()` → `TwoFactorSetupResponse`
- `confirm_2fa(totp_code)` → `dict`
- `disable_2fa(totp_code, password)` → `dict`
- `get_qr_code()` → `bytes`
- `debug_2fa()` → `dict`
- `refresh(refresh_token)` → `Token`
- `logout()` → `dict`

### WalletsClient

**Basic Wallet Operations:**

- `create_wallet(chain)` → `dict`
- `import_wallet(chain, private_key)` → `dict`
- `list_wallets()` → `List[dict]`
- `delete_wallet(wallet_id)` → `None`
- `get_balance(chain, address)` → `Decimal`

**Token Management:**

- `get_token_balance(wallet_id, token_address)` → `dict`
- `transfer_tokens(wallet_id, token_address, to_address, amount)` → `dict`
- `approve_tokens(wallet_id, token_address, spender_address, amount)` → `dict`

**Agent Wallets:**

- `deploy_agent_wallet()` → `dict`
- `list_agent_wallets()` → `List[dict]`
- `get_agent_wallet(address)` → `dict`
- `set_spending_limit(address, token, amount, period)` → `str`
- `update_whitelist(address, target, allowed)` → `str`
- `set_threshold(address, new_threshold)` → `str`
- `list_wallet_transactions(address)` → `List[dict]`

**DeFi Integration:**

- `swap_tokens(wallet_id, from_token, to_token, amount, slippage_tolerance)` → `dict`
- `deposit_yield_vault(wallet_id, vault_address, token_address, amount)` → `dict`
- `withdraw_yield_vault(wallet_id, vault_address, amount)` → `dict`
- `get_yield_positions(wallet_id)` → `List[dict]`

**Email Integration:**

- `list_email_accounts()` → `List[dict]`
- `create_email_account(provider, email_address, config)` → `dict`
- `test_email_connection(account_id)` → `dict`
- `get_inbox(account_id, limit=10, unread_only=False)` → `dict`

**Gas & Fees:**

- `sponsor_gas(token_address, amount)` → `str`
- `get_gas_sponsorship_balance()` → `Decimal`
- `send_user_operation(user_op, entry_point_address)` → `dict`

**Events & Monitoring:**

- `subscribe_to_events(wallet_address, event_types)` → `dict`
- `get_wallet_events(wallet_address, limit=50)` → `List[dict]`
- `unsubscribe_event(subscription_id)` → `None`

**RWA & NFTs:**

- `register_rwa_asset(token_address, token_id, metadata_uri)` → `dict`
- `list_rwa_assets()` → `List[dict]`
- `transfer_rwa(wallet_id, token_address, token_id, to_address, amount)` → `dict`
- `list_nfts(wallet_id)` → `List[dict]`
- `transfer_nft(wallet_id, contract_address, token_id, to_address)` → `dict`

**Fiat Integration:**

- `create_onramp_session(currency, amount)` → `dict`
- `get_onramp_status(session_id)` → `dict`

### AgentsClient

- `list_agents()` → `List[dict]`
- `create_agent(name, description, agent_type, parent_id=None, capabilities=[])` → `dict`
- `get_agent(agent_id)` → `dict`
- `update_agent(agent_id, **kwargs)` → `dict`
- `delete_agent(agent_id)` → `None`
- `get_inherited_rules(child_id)` → `dict`
- `delegate_task(master_id, child_agent_id, task_type, budget_allocation, deadline, parameters)` → `dict`
- `list_delegations(agent_id)` → `List[dict]`
- `provision_email_asset(child_id, email_account_id, permissions, quota)` → `dict`
- `provision_wallet_asset(child_id, chain)` → `dict`
- `transfer_assets_to_child(child_id, from_wallet, to_wallet, asset_type, amount, note)` → `dict`
- `get_email_usage(child_id)` → `dict`

### BridgeClient

- `get_quote(from_chain, to_chain, from_token, to_token, amount)` → `dict`
- `bridge_transfer(provider, from_chain, to_chain, from_token, to_token, amount, recipient_address)` → `dict`

### AssetsClient

- `get_multi_chain_asset_view()` → `dict`

### GovernanceClient

- `create_proposal(targets, values, calldatas, description)` → `dict`
- `cast_vote(proposal_id, support)` → `dict`
- `get_proposal_state(proposal_id)` → `dict`
- `get_user_votes()` → `List[dict]`

### ReputationClient

- `issue_sbt(to_address, metadata_uri)` → `dict`
- `get_sbt_owner(token_id)` → `dict`
- `get_user_reputation(user_id)` → `dict`
- `stake_reputation(amount)` → `dict`

### MonitoringClient

- `watch_address(address, alert_conditions)` → `dict`
- `get_transaction_status(tx_hash)` → `dict`
- `list_watches()` → `List[dict]`
- `get_alerts()` → `List[dict]`

### ComplianceClient

- `get_kyc_status()` → `dict`
- `initiate_kyc()` → `dict`
- `generate_report(start_date, end_date, report_type)` → `dict`
- `get_audit_trail(entity_id, entity_type)` → `List[dict]`

### SwapClient

- `get_quote(from_token, to_token, amount)` → `dict`
- `execute_swap(from_token, to_token, amount, slippage_tolerance)` → `dict`
- `cancel_swap(quote_id)` → `dict`

### MarketplaceClient

- `list_listings(limit=None)` → `List[dict]`
- `get_listing(listing_id)` → `dict`
- `create_listing(asset_id, price, quantity)` → `dict`
- `place_bid(listing_id, bid_amount)` → `dict`
- `cancel_listing(listing_id)` → `None`

### Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Running tests and linting
- Submitting pull requests
- Code style guidelines

---

## 📋 Requirements

- **Python 3.8+**
- **requests** or **httpx** (for async support)
- **pydantic** for data validation
- **Authenticator app** (Google Authenticator, Authy, Microsoft Authenticator, etc.)

---

## 📈 What's New in July 2025

### 🔥 Latest Features

- ✅ **Complete Two-Factor Authentication** with TOTP and SMS support
- ✅ **Agent Smart Contract Wallets** with programmable on-chain rules  
- ✅ **Master/Child Agent Hierarchy** with rule inheritance
- ✅ **Multi-Chain Asset Aggregation** across 10+ blockchains
- ✅ **Advanced DeFi Integration** with yield farming and swaps
- ✅ **Real-World Asset Tokenization** for physical asset management
- ✅ **Gas Abstraction** with ERC-4337 support
- ✅ **Enhanced Compliance** with KYC/AML and audit trails
- ✅ **Email Integration** via IMAP/SMTP and OAuth
- ✅ **Cross-Chain Bridging** for seamless asset transfers

### 🎯 Coming Soon

- 🔜 **Advanced AI Agent Templates** for common use cases
- 🔜 **Mobile SDK** for iOS and Android
- 🔜 **WebSocket Support** for real-time events
- 🔜 **Advanced Analytics** with machine learning insights
- 🔜 **Layer 2 Optimizations** for faster, cheaper transactions

---

**🎉 Ready to build the future of autonomous AI agents? Install the CirtusAI SDK today and unlock the complete power of programmable, compliant, and secure AI automation!**

```bash
pip install cirtusai-sdk
```

*Built with ❤️ by the CirtusAI team - Empowering the Autonomous*
