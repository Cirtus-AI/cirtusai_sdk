# CirtusAI SDK Agent Management Guide

## Overview

The CirtusAI SDK provides comprehensive agent management capabilities for both master and child agents. The agent system enables hierarchical agent architectures with granular permission management and asset provisioning.

## Features

- **Master Agent Management**: Core agent lifecycle operations
- **Child Agent Creation**: Hierarchical agent structures
- **Permission Management**: Granular access control for child agents
- **Asset Provisioning**: Automated email and wallet provisioning
- **Agent Linking**: Parent-child relationship management

## Agent Types

### Master Agents
- Primary user agents with full permissions
- Can create and manage child agents
- Have direct API access and authentication

### Child Agents
- Subordinate agents with limited, delegated permissions
- Created and managed by master agents
- Inherit specific permissions from parent
- Can have assets (email, wallets) provisioned automatically

## Basic Agent Operations

### List All Agents

```python
from cirtusai import CirtusAIClient

client = CirtusAIClient("https://api.cirtusai.com")
client.set_token("your_access_token")

# List all master agents for logged-in user
agents = client.agents.list_agents()
for agent in agents:
    print(f"Agent ID: {agent['id']}")
    print(f"Name: {agent['name']}")
    print(f"Status: {agent['status']}")
```

### Get Specific Agent

```python
# Retrieve specific agent details
agent_id = "agent_123"
agent = client.agents.get_agent(agent_id)

print(f"Agent Type: {agent['type']}")
print(f"Permissions: {agent.get('permissions_granted', [])}")
print(f"Created: {agent['created_at']}")
```

### Delete Agent

```python
# Delete an agent (master or child)
client.agents.delete_agent("agent_123")
print("Agent deleted successfully")
```

## Child Agent Management

### Create Child Agent

```python
# Create a new child agent with specific permissions
child_agent = client.agents.create_child_agent(
    parent_id="master_agent_123",
    name="Email Processing Agent",
    permissions_granted=["email:read", "email:send"]
)

print(f"Child Agent ID: {child_agent['id']}")
print(f"Parent ID: {child_agent['parent_id']}")
print(f"Permissions: {child_agent['permissions_granted']}")
```

### List Child Agents

```python
# Get all child agents for the current master agent
children = client.agents.get_children()
for child in children:
    print(f"Child ID: {child['id']}")
    print(f"Name: {child['name']}")
    print(f"Permissions: {child['permissions_granted']}")
```

### Update Child Permissions

```python
# Update permissions for a child agent
new_permissions = {
    "email:read": True,
    "email:send": True,
    "wallet:read": True,
    "wallet:send": False
}

updated_agent = client.agents.update_child_permissions(
    child_id="child_agent_456",
    permissions=new_permissions
)

print(f"Updated permissions: {updated_agent['permissions']}")
```

### Unlink Child Agent

```python
# Remove/delete a child agent
client.agents.unlink_child_agent("child_agent_456")
print("Child agent unlinked successfully")
```

## Asset Provisioning

### Provision Email Assets

```python
# Automatically provision email capability for a child agent
email_asset = client.agents.provision_email("child_agent_456")

print(f"Email provisioned: {email_asset['email_address']}")
print(f"Provider: {email_asset['provider']}")
print(f"Status: {email_asset['status']}")
```

### Provision Wallet Assets

```python
# Provision crypto wallet for child agent
wallet_asset = client.agents.provision_wallet(
    agent_id="child_agent_456",
    chain="ethereum"  # or "polygon", "arbitrum", etc.
)

print(f"Wallet Address: {wallet_asset['address']}")
print(f"Chain: {wallet_asset['chain']}")
print(f"Balance: {wallet_asset['balance']}")
```

## Advanced Agent Workflows

### Multi-Purpose Agent Creation

```python
def create_comprehensive_agent(client, parent_id, name):
    """Create a child agent with email and wallet capabilities"""
    
    # Step 1: Create child agent
    child = client.agents.create_child_agent(
        parent_id=parent_id,
        name=name,
        permissions_granted=[
            "email:read", "email:send",
            "wallet:read", "wallet:send"
        ]
    )
    
    child_id = child['id']
    print(f"Created child agent: {child_id}")
    
    # Step 2: Provision email
    try:
        email_asset = client.agents.provision_email(child_id)
        print(f"Email provisioned: {email_asset['email_address']}")
    except Exception as e:
        print(f"Email provisioning failed: {e}")
    
    # Step 3: Provision wallet
    try:
        wallet_asset = client.agents.provision_wallet(child_id, "ethereum")
        print(f"Wallet provisioned: {wallet_asset['address']}")
    except Exception as e:
        print(f"Wallet provisioning failed: {e}")
    
    return child

# Usage
master_agent_id = "master_123"
agent = create_comprehensive_agent(
    client, 
    master_agent_id, 
    "Trading Assistant Agent"
)
```

### Agent Permission Matrix

```python
def setup_permission_matrix(client, child_id, role):
    """Setup permissions based on agent role"""
    
    permission_templates = {
        "email_only": {
            "email:read": True,
            "email:send": True,
            "wallet:read": False,
            "wallet:send": False
        },
        "wallet_only": {
            "email:read": False,
            "email:send": False,
            "wallet:read": True,
            "wallet:send": True
        },
        "full_access": {
            "email:read": True,
            "email:send": True,
            "wallet:read": True,
            "wallet:send": True
        },
        "read_only": {
            "email:read": True,
            "email:send": False,
            "wallet:read": True,
            "wallet:send": False
        }
    }
    
    permissions = permission_templates.get(role, permission_templates["read_only"])
    return client.agents.update_child_permissions(child_id, permissions)

# Usage examples
setup_permission_matrix(client, "child_123", "email_only")
setup_permission_matrix(client, "child_456", "full_access")
```

### Bulk Agent Management

```python
def create_agent_fleet(client, parent_id, agent_configs):
    """Create multiple child agents with different configurations"""
    
    created_agents = []
    
    for config in agent_configs:
        try:
            # Create child agent
            child = client.agents.create_child_agent(
                parent_id=parent_id,
                name=config["name"],
                permissions_granted=config["permissions"]
            )
            
            # Provision assets based on config
            if config.get("needs_email"):
                client.agents.provision_email(child['id'])
            
            if config.get("needs_wallet"):
                client.agents.provision_wallet(
                    child['id'], 
                    config.get("chain", "ethereum")
                )
            
            created_agents.append(child)
            print(f"Created agent: {child['name']} ({child['id']})")
            
        except Exception as e:
            print(f"Failed to create agent {config['name']}: {e}")
    
    return created_agents

# Usage
agent_configs = [
    {
        "name": "Email Monitor Agent",
        "permissions": ["email:read"],
        "needs_email": True,
        "needs_wallet": False
    },
    {
        "name": "Trading Agent",
        "permissions": ["wallet:read", "wallet:send"],
        "needs_email": False,
        "needs_wallet": True,
        "chain": "ethereum"
    },
    {
        "name": "Notification Agent",
        "permissions": ["email:read", "email:send"],
        "needs_email": True,
        "needs_wallet": False
    }
]

fleet = create_agent_fleet(client, "master_123", agent_configs)
```

## Agent Monitoring and Status

### Agent Health Check

```python
def check_agent_health(client, agent_id):
    """Check agent status and asset health"""
    
    try:
        agent = client.agents.get_agent(agent_id)
        health_report = {
            "agent_id": agent_id,
            "status": agent.get("status", "unknown"),
            "permissions": agent.get("permissions_granted", []),
            "assets": {
                "email": False,
                "wallet": False
            }
        }
        
        # Check if agent has email capabilities
        if "email:read" in agent.get("permissions_granted", []):
            try:
                # Try to access email
                client.email.read_inbox(agent_id)
                health_report["assets"]["email"] = True
            except:
                health_report["assets"]["email"] = False
        
        # Check if agent has wallet capabilities
        if "wallet:read" in agent.get("permissions_granted", []):
            try:
                # Try to access wallet
                client.wallets.list_wallets()
                health_report["assets"]["wallet"] = True
            except:
                health_report["assets"]["wallet"] = False
        
        return health_report
        
    except Exception as e:
        return {"agent_id": agent_id, "error": str(e)}

# Usage
health = check_agent_health(client, "child_agent_123")
print(f"Agent Health: {health}")
```

### Agent Activity Monitoring

```python
def monitor_agent_activity(client):
    """Monitor all agent activity"""
    
    agents = client.agents.list_agents()
    children = client.agents.get_children()
    
    print("=== Agent Activity Report ===")
    print(f"Master Agents: {len(agents)}")
    print(f"Child Agents: {len(children)}")
    
    for child in children:
        permissions = child.get('permissions_granted', [])
        print(f"\nChild Agent: {child['name']}")
        print(f"  ID: {child['id']}")
        print(f"  Permissions: {', '.join(permissions)}")
        
        # Check recent activity (if available)
        health = check_agent_health(client, child['id'])
        print(f"  Email Active: {health['assets']['email']}")
        print(f"  Wallet Active: {health['assets']['wallet']}")

# Usage
monitor_agent_activity(client)
```

## Error Handling

### Common Error Scenarios

```python
def safe_agent_operation(client, operation, *args, **kwargs):
    """Safely execute agent operations with error handling"""
    
    try:
        result = getattr(client.agents, operation)(*args, **kwargs)
        return {"success": True, "result": result}
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            return {"success": False, "error": "Permission denied"}
        elif e.response.status_code == 404:
            return {"success": False, "error": "Agent not found"}
        else:
            return {"success": False, "error": f"HTTP error: {e}"}
    
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e}"}

# Usage examples
result = safe_agent_operation(client, "get_agent", "invalid_agent_id")
if not result["success"]:
    print(f"Operation failed: {result['error']}")
```

## Best Practices

### 1. Agent Naming Convention

```python
def generate_agent_name(purpose, environment="prod"):
    """Generate standardized agent names"""
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"{environment}_{purpose}_{timestamp}"

# Examples
email_agent = generate_agent_name("email_processor", "dev")
trading_agent = generate_agent_name("trading_bot", "prod")
```

### 2. Permission Management

```python
class PermissionManager:
    """Manage agent permissions systematically"""
    
    PERMISSION_LEVELS = {
        "minimal": ["email:read"],
        "standard": ["email:read", "email:send"],
        "advanced": ["email:read", "email:send", "wallet:read"],
        "full": ["email:read", "email:send", "wallet:read", "wallet:send"]
    }
    
    @classmethod
    def get_permissions(cls, level):
        return cls.PERMISSION_LEVELS.get(level, cls.PERMISSION_LEVELS["minimal"])
    
    @classmethod
    def validate_permissions(cls, permissions):
        valid_permissions = [
            "email:read", "email:send",
            "wallet:read", "wallet:send"
        ]
        return all(perm in valid_permissions for perm in permissions)

# Usage
permissions = PermissionManager.get_permissions("standard")
child = client.agents.create_child_agent(
    parent_id="master_123",
    name="Standard Agent",
    permissions_granted=permissions
)
```

### 3. Asset Lifecycle Management

```python
class AgentAssetManager:
    """Manage agent assets throughout lifecycle"""
    
    def __init__(self, client):
        self.client = client
    
    def setup_complete_agent(self, parent_id, name, needs_email=True, needs_wallet=True):
        """Setup agent with all required assets"""
        
        # Determine permissions based on needs
        permissions = []
        if needs_email:
            permissions.extend(["email:read", "email:send"])
        if needs_wallet:
            permissions.extend(["wallet:read", "wallet:send"])
        
        # Create agent
        agent = self.client.agents.create_child_agent(
            parent_id=parent_id,
            name=name,
            permissions_granted=permissions
        )
        
        agent_id = agent['id']
        
        # Provision assets
        if needs_email:
            self.client.agents.provision_email(agent_id)
        
        if needs_wallet:
            self.client.agents.provision_wallet(agent_id)
        
        return agent
    
    def cleanup_agent(self, agent_id):
        """Clean up agent and its assets"""
        try:
            self.client.agents.unlink_child_agent(agent_id)
            return True
        except Exception as e:
            print(f"Cleanup failed: {e}")
            return False

# Usage
manager = AgentAssetManager(client)
agent = manager.setup_complete_agent(
    parent_id="master_123",
    name="Complete Agent",
    needs_email=True,
    needs_wallet=True
)
```

## API Reference

### AgentsClient Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list_agents()` | List all master agents | - | List[Dict] |
| `get_agent()` | Get specific agent details | agent_id | Dict |
| `create_child_agent()` | Create new child agent | parent_id, name, permissions_granted | Dict |
| `delete_agent()` | Delete agent | agent_id | None |
| `provision_email()` | Provision email for child agent | agent_id | Dict |
| `provision_wallet()` | Provision wallet for child agent | agent_id, chain | Dict |
| `get_children()` | List all child agents | - | List[Dict] |
| `update_child_permissions()` | Update child permissions | child_id, permissions | Dict |
| `unlink_child_agent()` | Remove child agent | child_id | None |

### Agent Object Structure

```python
{
    "id": "agent_123",
    "name": "My Agent",
    "type": "master" | "child",
    "status": "active" | "inactive",
    "parent_id": "master_123",  # for child agents
    "permissions_granted": ["email:read", "email:send"],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### Available Permissions

- `email:read` - Read email messages
- `email:send` - Send email messages  
- `wallet:read` - View wallet balances and transactions
- `wallet:send` - Execute wallet transactions
