from pydantic import BaseModel, Field, EmailStr, StrictBool
from typing import List, Dict, Any, Optional

class Agent(BaseModel):
    id: str
    name: Optional[str]
    did: Optional[str]
    state: Optional[Dict[str, Any]]

class Asset(BaseModel):
    id: str
    type: str
    details: Dict[str, Any]

class ChildAgent(BaseModel):
    id: str
    parent_id: Optional[str]
    name: Optional[str]
    permissions: Optional[Dict[str, Any]]
    state: Optional[Dict[str, Any]]

class Permissions(BaseModel):
    permissions: Dict[str, Any]

class DID(BaseModel):
    did: str
    info: Dict[str, Any]

class EmailAccount(BaseModel):
    id: str
    provider: str
    email_address: str
    config: Dict[str, Any]

class CredentialResponse(BaseModel):
    credential: Dict[str, Any]

# Two-Factor Authentication Schemas
class TwoFactorSetupResponse(BaseModel):
    """Response from 2FA setup containing QR code and backup codes."""
    secret: str
    qr_code_uri: str
    qr_code_image: str
    backup_codes: List[str]

class Token(BaseModel):
    """Standard JWT token response."""
    access_token: str
    token_type: str = "bearer"

class TwoFactorRequiredResponse(BaseModel):
    """Response when 2FA verification is required."""
    requires_2fa: StrictBool
    temporary_token: str
    preferred_method: str
    message: str

class TwoFactorVerifyRequest(BaseModel):
    """Request to verify 2FA code with temporary token."""
    temporary_token: str
    totp_code: str

class TwoFactorStatusResponse(BaseModel):
    """Current 2FA status for a user."""
    is_2fa_enabled: StrictBool
    preferred_2fa_method: Optional[str]
    is_sms_enabled: StrictBool

class TwoFactorDisableRequest(BaseModel):
    """Request to disable 2FA."""
    totp_code: str
    password: str

class UserRegister(BaseModel):
    """User registration request."""
    username: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=1)
    preferred_2fa_method: Optional[str] = Field(default="totp")
