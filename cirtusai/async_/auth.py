import httpx
from typing import Dict, Any, Union, Optional
from ..schemas import (
    Token, 
    TwoFactorRequiredResponse, 
    TwoFactorSetupResponse,
    TwoFactorStatusResponse,
    UserRegister,
    TwoFactorVerifyRequest,
    TwoFactorDisableRequest
)

class TwoFactorAuthenticationError(Exception):
    """Raised when 2FA verification fails."""
    pass

class AsyncAuthClient:
    """
    Async authentication client with comprehensive Two-Factor Authentication support.
    
    Features:
    - User registration with automatic 2FA setup
    - Two-step login flow for 2FA users
    - TOTP management and verification
    - SMS 2FA support (framework ready)
    - Debug and troubleshooting methods
    """
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self.client = client
        self.base_url = base_url.rstrip("/")

    async def register(self, username: str, email: str, password: str, 
                      preferred_2fa_method: str = "totp") -> TwoFactorSetupResponse:
        """
        Register a new user with automatic 2FA setup.
        
        Args:
            username: Unique username
            email: User's email address
            password: User's password
            preferred_2fa_method: Preferred 2FA method ('totp' or 'sms')
        
        Returns:
            TwoFactorSetupResponse with QR code and backup codes
        """
        url = f"{self.base_url}/auth/register"
        user_data = UserRegister(
            username=username,
            email=email,
            password=password,
            preferred_2fa_method=preferred_2fa_method
        )
        resp = await self.client.post(url, json=user_data.model_dump())
        resp.raise_for_status()
        return TwoFactorSetupResponse(**resp.json())

    async def login(self, username: str, password: str) -> Union[Token, TwoFactorRequiredResponse]:
        """
        Perform initial login - returns either immediate token or 2FA requirement.
        
        Args:
            username: Username or email
            password: User's password
        
        Returns:
            Token if 2FA not required, TwoFactorRequiredResponse if 2FA needed
        """
        url = f"{self.base_url}/auth/login"
        data = {"username": username, "password": password}
        resp = await self.client.post(url, data=data)
        resp.raise_for_status()
        
        response_data = resp.json()
        
        # Check if 2FA is required
        if response_data.get("requires_2fa"):
            return TwoFactorRequiredResponse(**response_data)
        else:
            return Token(**response_data)

    async def verify_2fa(self, temporary_token: str, totp_code: str) -> Token:
        """
        Complete 2FA verification and receive final access token.
        
        Args:
            temporary_token: Temporary token from login response
            totp_code: 6-digit TOTP code from authenticator app
        
        Returns:
            Token with final access token
            
        Raises:
            TwoFactorAuthenticationError: If 2FA verification fails
        """
        url = f"{self.base_url}/auth/verify-2fa"
        verify_request = TwoFactorVerifyRequest(
            temporary_token=temporary_token,
            totp_code=totp_code
        )
        resp = await self.client.post(url, json=verify_request.model_dump())
        # Raise custom exception on any error status code
        if resp.status_code >= 400:
            error_detail = resp.json().get("detail", "2FA verification failed")
            raise TwoFactorAuthenticationError(error_detail)
        return Token(**resp.json())

    async def login_with_2fa(self, username: str, password: str, totp_code: str) -> Token:
        """
        Convenience method for complete login flow with 2FA.
        
        Args:
            username: Username or email
            password: User's password
            totp_code: 6-digit TOTP code from authenticator app
        
        Returns:
            Token with final access token
            
        Raises:
            TwoFactorAuthenticationError: If any step of 2FA login fails
        """
        # Step 1: Initial login
        login_result = await self.login(username, password)
        
        # If no 2FA required, return token directly
        if isinstance(login_result, Token):
            return login_result
        
        # Step 2: Verify 2FA
        if isinstance(login_result, TwoFactorRequiredResponse):
            return await self.verify_2fa(login_result.temporary_token, totp_code)
        
        raise TwoFactorAuthenticationError("Unexpected login response")

    async def get_2fa_status(self) -> TwoFactorStatusResponse:
        """Get current 2FA status for authenticated user."""
        url = f"{self.base_url}/auth/2fa/status"
        resp = await self.client.get(url)
        resp.raise_for_status()
        return TwoFactorStatusResponse(**resp.json())

    async def setup_2fa(self) -> TwoFactorSetupResponse:
        """Set up 2FA for existing user (alternative to registration auto-setup)."""
        url = f"{self.base_url}/auth/2fa/setup"
        resp = await self.client.get(url)
        resp.raise_for_status()
        return TwoFactorSetupResponse(**resp.json())

    async def confirm_2fa(self, totp_code: str) -> Dict[str, str]:
        """Confirm and enable 2FA setup with verification code."""
        url = f"{self.base_url}/auth/2fa/confirm"
        resp = await self.client.post(url, json={"totp_code": totp_code})
        resp.raise_for_status()
        return resp.json()

    async def disable_2fa(self, totp_code: str, password: str) -> Dict[str, str]:
        """Disable 2FA for the current user."""
        url = f"{self.base_url}/auth/2fa/disable"
        disable_request = TwoFactorDisableRequest(
            totp_code=totp_code,
            password=password
        )
        resp = await self.client.post(url, json=disable_request.model_dump())
        resp.raise_for_status()
        return resp.json()

    async def get_qr_code(self) -> bytes:
        """Get QR code image as PNG bytes."""
        url = f"{self.base_url}/auth/2fa/qr"
        resp = await self.client.get(url)
        resp.raise_for_status()
        return resp.content

    async def request_sms_code(self) -> Dict[str, str]:
        """Request SMS code for SMS 2FA (when implemented)."""
        url = f"{self.base_url}/auth/2fa/request-sms"
        resp = await self.client.post(url)
        resp.raise_for_status()
        return resp.json()

    async def debug_2fa(self) -> Dict[str, Any]:
        """
        Debug TOTP setup and time sync issues (authenticated users only).
        
        Returns detailed information about current valid TOTP codes.
        """
        url = f"{self.base_url}/auth/debug-2fa"
        resp = await self.client.get(url)
        resp.raise_for_status()
        return resp.json()

    async def refresh(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh the access token using a valid refresh token."""
        url = f"{self.base_url}/auth/refresh"
        resp = await self.client.post(url, json={"refresh_token": refresh_token})
        resp.raise_for_status()
        return resp.json()
