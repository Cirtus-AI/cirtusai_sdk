# CirtusAI SDK Authentication Guide

## Overview

The CirtusAI SDK provides comprehensive authentication capabilities with robust Two-Factor Authentication (2FA) support. The authentication system supports TOTP-based 2FA, SMS verification (framework ready), and complete user lifecycle management.

## Features

- **User Registration**: Automatic 2FA setup during registration
- **Two-Step Login Flow**: Secure authentication for 2FA-enabled users
- **TOTP Management**: Complete TOTP setup, verification, and management
- **SMS 2FA Support**: Framework ready for SMS-based authentication
- **Debug Tools**: Troubleshooting and time sync verification tools
- **Token Management**: Access token refresh and lifecycle management

## Basic Authentication

### User Registration

Register a new user with automatic 2FA setup:

```python
from cirtusai import CirtusAIClient

client = CirtusAIClient("https://api.cirtusai.com")

# Register with automatic 2FA setup
setup_response = client.auth.register(
    username="your_username",
    email="your_email@example.com",
    password="your_secure_password",
    preferred_2fa_method="totp"  # or "sms"
)

print(f"QR Code URL: {setup_response.qr_code_url}")
print(f"Secret Key: {setup_response.secret_key}")
print(f"Backup Codes: {setup_response.backup_codes}")
```

### Simple Login (No 2FA)

For accounts without 2FA enabled:

```python
# Direct login without 2FA
token = client.auth.login("username", "password")
client.set_token(token.access_token)
```

## Two-Factor Authentication

### Login with 2FA

#### Method 1: Two-Step Process

```python
# Step 1: Initial login
login_result = client.auth.login("username", "password")

if hasattr(login_result, 'requires_2fa') and login_result.requires_2fa:
    # Step 2: Verify 2FA
    totp_code = input("Enter TOTP code: ")
    token = client.auth.verify_2fa(login_result.temporary_token, totp_code)
    client.set_token(token.access_token)
else:
    # No 2FA required
    client.set_token(login_result.access_token)
```

#### Method 2: Single Method

```python
# Complete 2FA login in one call
try:
    token = client.auth.login_with_2fa("username", "password", "123456")
    client.set_token(token.access_token)
    print("Login successful!")
except TwoFactorAuthenticationError as e:
    print(f"2FA verification failed: {e}")
```

### 2FA Management

#### Check 2FA Status

```python
status = client.auth.get_2fa_status()
print(f"2FA Enabled: {status.enabled}")
print(f"Method: {status.method}")
print(f"Backup Codes Available: {status.backup_codes_remaining}")
```

#### Setup 2FA for Existing User

```python
# Setup 2FA
setup_response = client.auth.setup_2fa()
print(f"Scan this QR code: {setup_response.qr_code_url}")

# After scanning QR code, confirm with TOTP
totp_code = input("Enter TOTP code from authenticator app: ")
result = client.auth.confirm_2fa(totp_code)
print(f"2FA setup complete: {result}")
```

#### Disable 2FA

```python
# Disable 2FA (requires current TOTP code and password)
totp_code = input("Enter current TOTP code: ")
password = input("Enter your password: ")

result = client.auth.disable_2fa(totp_code, password)
print(f"2FA disabled: {result}")
```

#### Get QR Code Image

```python
# Get QR code as PNG bytes
qr_bytes = client.auth.get_qr_code()
with open("qr_code.png", "wb") as f:
    f.write(qr_bytes)
```

## SMS 2FA (Framework Ready)

```python
# Request SMS code (when implemented)
result = client.auth.request_sms_code()
print(f"SMS sent: {result}")
```

## Debugging and Troubleshooting

### Debug TOTP Issues

```python
# Debug TOTP setup and time sync
debug_info = client.auth.debug_2fa()
print(f"Current valid codes: {debug_info.get('valid_codes')}")
print(f"Server time: {debug_info.get('server_time')}")
print(f"Time window: {debug_info.get('time_window')}")
```

## Token Management

### Refresh Access Token

```python
# Refresh expired access token
refresh_token = "your_refresh_token"
new_tokens = client.auth.refresh(refresh_token)
client.set_token(new_tokens["access_token"])
```

## Error Handling

### Custom Exception Handling

```python
from cirtusai.auth import TwoFactorAuthenticationError

try:
    token = client.auth.login_with_2fa("username", "password", "invalid_code")
except TwoFactorAuthenticationError as e:
    print(f"2FA Error: {e}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
```

## Advanced Usage

### Complete Registration and Login Flow

```python
def complete_registration_flow():
    client = CirtusAIClient("https://api.cirtusai.com")
    
    # Register user
    setup = client.auth.register(
        username="new_user",
        email="user@example.com",
        password="secure_password"
    )
    
    print("Please scan this QR code with your authenticator app:")
    print(setup.qr_code_url)
    
    # Wait for user to setup authenticator
    totp_code = input("Enter TOTP code to confirm setup: ")
    client.auth.confirm_2fa(totp_code)
    
    # Now login with 2FA
    token = client.auth.login_with_2fa("new_user", "secure_password", totp_code)
    client.set_token(token.access_token)
    
    return client
```

### Session Management

```python
class AuthenticatedSession:
    def __init__(self, base_url, username, password):
        self.client = CirtusAIClient(base_url)
        self.username = username
        self.password = password
        self._authenticate()
    
    def _authenticate(self):
        login_result = self.client.auth.login(self.username, self.password)
        
        if hasattr(login_result, 'requires_2fa'):
            totp_code = input("Enter TOTP code: ")
            token = self.client.auth.verify_2fa(
                login_result.temporary_token, 
                totp_code
            )
        else:
            token = login_result
            
        self.client.set_token(token.access_token)
    
    def get_client(self):
        return self.client
```

## Security Best Practices

### 1. Secure Token Storage

```python
import keyring

# Store tokens securely
def store_token_securely(token):
    keyring.set_password("cirtusai", "access_token", token)

def get_stored_token():
    return keyring.get_password("cirtusai", "access_token")
```

### 2. Automatic Token Refresh

```python
def auto_refresh_client(client, refresh_token):
    try:
        # Attempt API call
        response = client.some_api_call()
        return response
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            # Token expired, refresh
            new_tokens = client.auth.refresh(refresh_token)
            client.set_token(new_tokens["access_token"])
            # Retry original call
            return client.some_api_call()
        raise
```

### 3. Backup Code Management

```python
def save_backup_codes(backup_codes):
    """Save backup codes securely"""
    with open("backup_codes.txt", "w") as f:
        f.write("CirtusAI Backup Codes (Store Securely):\n")
        for i, code in enumerate(backup_codes, 1):
            f.write(f"{i}. {code}\n")
    print("Backup codes saved to backup_codes.txt - store this file securely!")
```

## Configuration

### Environment Variables

```python
import os
from cirtusai import CirtusAIClient

# Configure using environment variables
client = CirtusAIClient(
    base_url=os.getenv("CIRTUSAI_API_URL", "https://api.cirtusai.com"),
    token=os.getenv("CIRTUSAI_ACCESS_TOKEN")
)
```

### Configuration File

```python
import json

def load_auth_config(config_file="cirtusai_config.json"):
    with open(config_file) as f:
        config = json.load(f)
    
    client = CirtusAIClient(config["base_url"])
    
    if config.get("auto_login"):
        token = client.auth.login_with_2fa(
            config["username"],
            config["password"],
            input("Enter TOTP code: ")
        )
        client.set_token(token.access_token)
    
    return client
```

## API Reference

### AuthClient Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `register()` | Register new user with 2FA | username, email, password, preferred_2fa_method | TwoFactorSetupResponse |
| `login()` | Initial login step | username, password | Token or TwoFactorRequiredResponse |
| `verify_2fa()` | Complete 2FA verification | temporary_token, totp_code | Token |
| `login_with_2fa()` | Complete 2FA login flow | username, password, totp_code | Token |
| `get_2fa_status()` | Get current 2FA status | - | TwoFactorStatusResponse |
| `setup_2fa()` | Setup 2FA for existing user | - | TwoFactorSetupResponse |
| `confirm_2fa()` | Confirm 2FA setup | totp_code | Dict |
| `disable_2fa()` | Disable 2FA | totp_code, password | Dict |
| `get_qr_code()` | Get QR code image | - | bytes |
| `request_sms_code()` | Request SMS code | - | Dict |
| `debug_2fa()` | Debug TOTP issues | - | Dict |
| `refresh()` | Refresh access token | refresh_token | Dict |

### Response Models

#### Token
```python
{
    "access_token": "string",
    "token_type": "bearer",
    "expires_in": 3600,
    "refresh_token": "string"
}
```

#### TwoFactorRequiredResponse
```python
{
    "requires_2fa": true,
    "temporary_token": "string",
    "message": "2FA verification required"
}
```

#### TwoFactorSetupResponse
```python
{
    "secret_key": "string",
    "qr_code_url": "string",
    "backup_codes": ["code1", "code2", ...],
    "manual_entry_key": "string"
}
```
