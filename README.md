# CirtusAI Python SDK (Updated July 2025)

The CirtusAI Python SDK provides a simple, robust interface for developers to interact with the CirtusAI platform with **comprehensive Two-Factor Authentication support**. It enables seamless agent management, wallet and asset provisioning, decentralized identity (DID) operations, and verifiable credential workflows—all through a modern, well-documented Python API and CLI.

- **Complete 2FA Support:** TOTP-based authentication with QR code setup
- **Sync and async support:** Use either synchronous or asynchronous clients
- **Enhanced Security:** Mandatory 2FA for all new accounts with time sync tolerance
- **Comprehensive CLI:** Manage agents, wallets, and credentials from the command line
- **Pydantic models:** Typed request/response validation for reliability
- **Easy integration:** Designed for third-party developers to get started in minutes
- **Automated tests and CI:** Ensures reliability and compatibility with the CirtusAI platform

Whether you're building identity-driven apps, automating agent provisioning, or issuing verifiable credentials, the CirtusAI SDK makes integration fast and developer-friendly with enterprise-grade security.

---

## Installation

```bash
pip install cirtusai-sdk
# or to install the dev extras:
pip install cirtusai-sdk[dev]
```

---

## Quickstart with Two-Factor Authentication

### Registration and 2FA Setup
```python
from cirtusai import CirtusAIClient
from cirtusai.auth import TwoFactorAuthenticationError

# Initialize client
client = CirtusAIClient(base_url="http://localhost:8000")

# Register new user (automatic 2FA setup)
# The username is for logging in, the email is for communication and recovery.
setup_info = client.auth.register(
    username="newuser",
    email="user@example.com",
    password="SecurePass123!",
    preferred_2fa_method="totp"
)

# Save QR code for authenticator app
print(f"Scan this QR code: data:image/png;base64,{setup_info.qr_code_image}")
print(f"Or enter this secret manually: {setup_info.secret}")
print(f"Backup codes: {setup_info.backup_codes}")
```

### Login with 2FA

```python
# Method 1: Two-step login (recommended for interactive apps)
login_result = client.auth.login("newuser", "SecurePass123!")

if hasattr(login_result, 'requires_2fa') and login_result.requires_2fa:
    # Get TOTP code from user's authenticator app
    totp_code = input("Enter your 6-digit code from authenticator app: ")
    
    # Complete 2FA verification
    token = client.auth.verify_2fa(login_result.temporary_token, totp_code)
    
    # Set token for authenticated requests
    client.set_token(token.access_token)
else:
    # User doesn't have 2FA enabled
    client.set_token(login_result.access_token)

# Method 2: One-step login (if you have the TOTP code)
try:
    token = client.auth.login_with_2fa(
        "newuser", 
        "SecurePass123!", 
        "123456"  # Current TOTP code
    )
    client.set_token(token.access_token)
except TwoFactorAuthenticationError as e:
    print(f"2FA failed: {e}")
```

### Using Authenticated Client

```python
# Now you can use all authenticated features
agents = client.agents.list_agents()
child = client.agents.create_child_agent(parent_id=agents[0]["id"], name="MyChild")
email_asset = client.agents.provision_email(child["id"])

# 2FA management
status = client.auth.get_2fa_status()
print(f"2FA enabled: {status.is_2fa_enabled}")

client.close()
```

---

## Advanced 2FA Features

### Debugging Time Sync Issues

```python
# Check current valid TOTP codes
debug_info = client.auth.debug_2fa()
print("Valid codes right now:")
for step, code in debug_info["valid_codes"].items():
    print(f"  {step}: {code}")
```

### Managing 2FA Settings

```python
# Get current 2FA status
status = client.auth.get_2fa_status()

# Get QR code for existing setup
qr_bytes = client.auth.get_qr_code()
with open("qr_code.png", "wb") as f:
    f.write(qr_bytes)

# Disable 2FA (requires password + current TOTP code)
result = client.auth.disable_2fa(
    totp_code="123456",
    password="SecurePass123!"
)
```

---

## Async Client Example

```python
import asyncio
from cirtusai.async_ import AsyncCirtusAIClient

async def main():
    client = AsyncCirtusAIClient(base_url="http://localhost:8000")
    
    # Register with 2FA
    setup_info = await client.auth.register(
        username="asyncuser",
        email="async@example.com", 
        password="SecurePass123!"
    )
    
    # Login with 2FA
    token = await client.auth.login_with_2fa(
        "async@example.com",
        "SecurePass123!",
        "123456"
    )
    
    await client.set_token(token.access_token)
    
    # Use authenticated features
    status = await client.auth.get_2fa_status()
    print(f"2FA Status: {status}")
    
    await client.close()

asyncio.run(main())
```

---

## API Reference

### `AuthClient` / `AsyncAuthClient`

All methods are available on both the synchronous `client.auth` and the asynchronous `await client.auth` objects.

#### Registration & Login

- **`register(username, email, password, preferred_2fa_method?)`**: Registers a new user and returns a `TwoFactorSetupResponse` with a secret, QR code, and backup codes.
- **`login(username, password)`**: Initiates login. The `username` can be the username or email address. Returns a `Token` for non-2FA users or a `TwoFactorRequiredResponse` for 2FA-enabled users.
- **`login_with_2fa(username, password, totp_code)`**: A convenience method to perform a complete 2FA login in one step. The `username` can be the username or email address. Returns a `Token`.
- **`verify_2fa(temporary_token, totp_code)`**: Verifies the TOTP code using the temporary token from the `login` response. Returns the final `Token`.
- **`refresh(refresh_token)`**: Refreshes an expired access token. Returns a new `Token` object.

#### 2FA Management

- **`get_2fa_status()`**: Returns a `TwoFactorStatusResponse` indicating if 2FA is enabled.
- **`setup_2fa()`**: Initiates 2FA setup for an existing user. Returns a `TwoFactorSetupResponse`.
- **`confirm_2fa(totp_code)`**: Confirms and enables 2FA after setup.
- **`disable_2fa(totp_code, password)`**: Disables 2FA for the account. Requires both a valid TOTP code and the user's password.
- **`get_qr_code()`**: Returns the user's current 2FA QR code as `bytes`.
- **`debug_2fa()`**: Returns a dictionary with debugging information, including currently valid TOTP codes, to help troubleshoot time sync issues.

### Pydantic Schemas

The SDK uses Pydantic models for robust type validation. The following 2FA-related schemas are available under `cirtusai.schemas`:

- `Token`: Contains `access_token`, `refresh_token`, and `token_type`.
- `UserRegister`: Schema for the registration request.
- `TwoFactorSetupResponse`: Contains the secret, QR code, and backup codes for setting up 2FA.
- `TwoFactorRequiredResponse`: Indicates that a second factor is required to complete login.
- `TwoFactorVerifyRequest`: The request to verify a TOTP code.
- `TwoFactorStatusResponse`: The current 2FA status of a user account.
- `TwoFactorDisableRequest`: The request to disable 2FA.

---

## Features

### Authentication & Security

- ✅ **Complete Two-Factor Authentication (TOTP)**
- ✅ **User registration with automatic 2FA setup**
- ✅ **QR code generation for authenticator apps**
- ✅ **Time synchronization tolerance (±60 seconds)**
- ✅ **Comprehensive error handling and debugging**
- ✅ **Temporary token management for secure 2FA flow**

### Platform Features

- ✅ Manage agents and child agents
- ✅ Provision email and wallet assets
- ✅ Issue and verify verifiable credentials
- ✅ Full CLI for agent and asset management
- ✅ Sync and async Python API
- ✅ Pydantic data validation

---

## Command-Line Interface (CLI)

After installation, use the `cirtusai` command with 2FA support:

```bash
# Set your access token (get from login with 2FA)
export CIRTUSAI_TOKEN="your_access_token_here"

# Use CLI commands
cirtusai agents list
cirtusai agents provision-email

# CLI will prompt for 2FA during authentication
cirtusai auth login --username user@example.com
```

Run `cirtusai --help` for all commands.

---

## Error Handling

### 2FA-Specific Errors

```python
from cirtusai.auth import TwoFactorAuthenticationError

try:
    token = client.auth.verify_2fa(temp_token, "wrong_code")
except TwoFactorAuthenticationError as e:
    if "time_step" in str(e):
        print("Time sync issue - check your device time")
    elif "Invalid TOTP code" in str(e):
        print("Wrong code - try the current code from your authenticator app")
    else:
        print(f"2FA error: {e}")
```

### General HTTP Errors

```python
import requests
import httpx

try:
    result = client.auth.login("user@example.com", "wrong_password")
except requests.HTTPError as e: # For sync client
    if e.response.status_code == 401:
        print("Invalid credentials")
    else:
        print(f"HTTP error: {e}")
except httpx.HTTPStatusError as e: # For async client
    if e.response.status_code == 401:
        print("Invalid credentials")
    else:
        print(f"HTTP error: {e}")
```

---

## Requirements

- Python 3.8+
- `requests` or `httpx` (for async)
- `pydantic` for data validation
- Authenticator app (Google Authenticator, Authy, Microsoft Authenticator)

---

## Documentation

- [Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md): Advanced usage, API models, and error handling

---

## Security Considerations

- ✅ **Mandatory 2FA** for all new accounts
- ✅ **TOTP secrets encrypted** in database
- ✅ **Temporary tokens** with short expiration
- ✅ **Time sync tolerance** for real-world usage
- ✅ **Comprehensive error messages** for debugging
- ⚠️ **Store backup codes securely** - they're your account recovery method
- ⚠️ **Keep your authenticator app** synced with accurate time
- ⚠️ **Use HTTPS** in production environments

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

### Development Setup

```bash
pip install -e .[dev]
pytest
```

---

### July 2025 Update

- ✅ **Complete Two-Factor Authentication support**
- ✅ **Sync/async clients** for all 2FA methods
- ✅ **Updated schemas** and error handling
- ✅ **Comprehensive CLI** for 2FA management
- ✅ **Polished documentation** and examples
