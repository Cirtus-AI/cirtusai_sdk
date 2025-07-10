"""
Tests for the AsyncAuthClient with comprehensive 2FA functionality.
"""
import pytest
import httpx
import respx
from httpx import Response
import pytest_asyncio

from cirtusai.async_.auth import AsyncAuthClient, TwoFactorAuthenticationError
from cirtusai.schemas import (
    Token, 
    TwoFactorRequiredResponse, 
    TwoFactorSetupResponse,
    TwoFactorStatusResponse,
    UserRegister,
    TwoFactorVerifyRequest,
    TwoFactorDisableRequest
)

API_URL = "http://testserver"

@pytest_asyncio.fixture
def event_loop():
    """Override event_loop for pytest-asyncio"""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def auth_client():
    async with httpx.AsyncClient() as client:
        yield AsyncAuthClient(client, API_URL)


class TestAsyncUserRegistration:
    """Test async user registration with automatic 2FA setup."""
    
    @pytest.mark.asyncio
    async def test_register_user_success(self, auth_client):
        """Test successful user registration with 2FA setup."""
        expected_payload = {
            "username": "testuser",
            "email": "test@example.com", 
            "password": "SecurePass123!",
            "preferred_2fa_method": "totp"
        }
        
        response_data = {
            "secret": "JBSWY3DPEHPK3PXP",
            "qr_code_uri": "otpauth://totp/CirtusAI:test@example.com?secret=JBSWY3DPEHPK3PXP&issuer=CirtusAI",
            "qr_code_image": "iVBORw0KGgoAAAANSUhEUgAAAQEAAAEBCAYAAA...",
            "backup_codes": ["ABCD1234", "EFGH5678", "IJKL9012", "MNOP3456", "QRST7890", "UVWX1234", "YZAB5678", "CDEF9012"]
        }
        
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/register", json=expected_payload).respond(201, json=response_data)
            
            result = await auth_client.register(
                username="testuser",
                email="test@example.com",
                password="SecurePass123!",
                preferred_2fa_method="totp"
            )
            
            assert isinstance(result, TwoFactorSetupResponse)
            assert result.secret == "JBSWY3DPEHPK3PXP"
            assert "CirtusAI" in result.qr_code_uri
            assert len(result.backup_codes) == 8

    @pytest.mark.asyncio
    async def test_register_user_default_2fa_method(self, auth_client):
        """Test registration with default 2FA method."""
        expected_payload = {
            "username": "testuser",
            "email": "test@example.com", 
            "password": "SecurePass123!",
            "preferred_2fa_method": "totp"
        }
        
        response_data = {
            "secret": "JBSWY3DPEHPK3PXP",
            "qr_code_uri": "otpauth://totp/CirtusAI:test@example.com?secret=JBSWY3DPEHPK3PXP&issuer=CirtusAI",
            "qr_code_image": "iVBORw0KGgoAAAANSUhEUgAAAQEAAAEBCAYAAA...",
            "backup_codes": ["ABCD1234", "EFGH5678"]
        }
        
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/register", json=expected_payload).respond(201, json=response_data)
            
            result = await auth_client.register(
                username="testuser",
                email="test@example.com",
                password="SecurePass123!"
            )
            
            assert isinstance(result, TwoFactorSetupResponse)

    @pytest.mark.asyncio
    async def test_register_user_username_taken(self, auth_client):
        """Test registration failure when username is taken."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/register").respond(400, json={"detail": "Username already registered"})
            
            with pytest.raises(httpx.HTTPStatusError):
                await auth_client.register(
                    username="taken_username",
                    email="test@example.com",
                    password="SecurePass123!"
                )

    @pytest.mark.asyncio
    async def test_register_user_email_taken(self, auth_client):
        """Test registration failure when email is taken."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/register").respond(400, json={"detail": "Email already registered"})
            
            with pytest.raises(httpx.HTTPStatusError):
                await auth_client.register(
                    username="testuser",
                    email="taken@example.com",
                    password="SecurePass123!"
                )


class TestAsyncLoginFlow:
    """Test various login scenarios including 2FA flows."""

    @pytest.mark.asyncio
    async def test_login_without_2fa(self, auth_client):
        """Test login for legacy user without 2FA enabled."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/login").respond(200, json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer"
            })
            
            result = await auth_client.login("user@example.com", "password123")
            
            assert isinstance(result, Token)
            assert result.access_token.startswith("eyJ0eXA")
            assert result.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_login_with_2fa_required(self, auth_client):
        """Test login that requires 2FA verification."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/login").respond(200, json={
                "requires_2fa": True,
                "temporary_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.temp...",
                "preferred_method": "totp",
                "message": "2FA verification required. Use the temporary token in /auth/verify-2fa endpoint."
            })
            
            result = await auth_client.login("user@example.com", "password123")
            
            assert isinstance(result, TwoFactorRequiredResponse)
            assert result.requires_2fa is True
            assert result.temporary_token.startswith("eyJ0eXA")
            assert result.preferred_method == "totp"

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, auth_client):
        """Test login with invalid credentials."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/login").respond(401, json={"detail": "Incorrect username/email or password"})
            
            with pytest.raises(httpx.HTTPStatusError):
                await auth_client.login("wrong@example.com", "wrongpassword")


class TestAsyncTwoFactorVerification:
    """Test async 2FA verification flows."""

    @pytest.mark.asyncio
    async def test_verify_2fa_success(self, auth_client):
        """Test successful 2FA verification."""
        expected_payload = {
            "temporary_token": "temp_token_123",
            "totp_code": "123456"
        }
        
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/verify-2fa", json=expected_payload).respond(200, json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.final...",
                "token_type": "bearer"
            })
            
            result = await auth_client.verify_2fa("temp_token_123", "123456")
            
            assert isinstance(result, Token)
            assert result.access_token.startswith("eyJ0eXA")
            assert result.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_verify_2fa_invalid_code(self, auth_client):
        """Test 2FA verification with invalid TOTP code."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/verify-2fa").respond(401, json={
                "detail": "Invalid TOTP code '999999'. Valid codes right now: 123456, 789012, 345678. Check your authenticator app time sync."
            })
            
            with pytest.raises(TwoFactorAuthenticationError) as exc_info:
                await auth_client.verify_2fa("temp_token_123", "999999")
            
            assert "Invalid TOTP code" in str(exc_info.value)
            assert "Valid codes right now" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_verify_2fa_expired_token(self, auth_client):
        """Test 2FA verification with expired temporary token."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/verify-2fa").respond(401, json={"detail": "Invalid or expired temporary token"})
            
            with pytest.raises(TwoFactorAuthenticationError) as exc_info:
                await auth_client.verify_2fa("expired_token", "123456")
            
            assert "expired temporary token" in str(exc_info.value)


class TestAsyncConvenienceMethods:
    """Test convenience methods for complete login flows."""

    @pytest.mark.asyncio
    async def test_login_with_2fa_complete_flow(self, auth_client):
        """Test complete login flow with 2FA using convenience method."""
        async with respx.mock(base_url=API_URL) as route:
            # First call to login - returns 2FA requirement
            route.post("/auth/login").respond(200, json={
                "requires_2fa": True,
                "temporary_token": "temp_token_workflow",
                "preferred_method": "totp",
                "message": "2FA verification required."
            })
            
            # Second call to verify-2fa - returns final token
            route.post("/auth/verify-2fa").respond(200, json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.final...",
                "token_type": "bearer"
            })
            
            result = await auth_client.login_with_2fa("user@example.com", "password123", "123456")
            
            assert isinstance(result, Token)
            assert result.access_token.startswith("eyJ0eXA")

    @pytest.mark.asyncio
    async def test_login_with_2fa_no_2fa_required(self, auth_client):
        """Test convenience method when 2FA is not required."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/login").respond(200, json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.direct...",
                "token_type": "bearer"
            })
            
            result = await auth_client.login_with_2fa("legacy@example.com", "password123", "123456")
            
            assert isinstance(result, Token)
            assert result.access_token.startswith("eyJ0eXA")

    @pytest.mark.asyncio
    async def test_login_with_2fa_verification_fails(self, auth_client):
        """Test convenience method when 2FA verification fails."""
        async with respx.mock(base_url=API_URL) as route:
            # First call succeeds
            route.post("/auth/login").respond(200, json={
                "requires_2fa": True,
                "temporary_token": "temp_token_abc",
                "preferred_method": "totp",
                "message": "2FA verification required."
            })
            
            # Second call fails
            route.post("/auth/verify-2fa").respond(401, json={"detail": "Invalid TOTP code '999999'"})
            
            with pytest.raises(TwoFactorAuthenticationError):
                await auth_client.login_with_2fa("user@example.com", "password123", "999999")


class TestAsyncTwoFactorManagement:
    """Test async 2FA management endpoints."""

    @pytest.mark.asyncio
    async def test_get_2fa_status(self, auth_client):
        """Test getting 2FA status for authenticated user."""
        async with respx.mock(base_url=API_URL) as route:
            route.get("/auth/2fa/status").respond(200, json={
                "is_2fa_enabled": True,
                "preferred_2fa_method": "totp",
                "is_sms_enabled": False
            })
            
            result = await auth_client.get_2fa_status()
            
            assert isinstance(result, TwoFactorStatusResponse)
            assert result.is_2fa_enabled is True
            assert result.preferred_2fa_method == "totp"
            assert result.is_sms_enabled is False

    @pytest.mark.asyncio
    async def test_setup_2fa(self, auth_client):
        """Test setting up 2FA for existing user."""
        async with respx.mock(base_url=API_URL) as route:
            route.get("/auth/2fa/setup").respond(200, json={
                "secret": "JBSWY3DPEHPK3PXP",
                "qr_code_uri": "otpauth://totp/CirtusAI:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=CirtusAI",
                "qr_code_image": "iVBORw0KGgoAAAANSUhEUgAAAQEAAAEBCAYAAA...",
                "backup_codes": ["CODE1", "CODE2", "CODE3", "CODE4", "CODE5", "CODE6", "CODE7", "CODE8"]
            })
            
            result = await auth_client.setup_2fa()
            
            assert isinstance(result, TwoFactorSetupResponse)
            assert result.secret == "JBSWY3DPEHPK3PXP"
            assert len(result.backup_codes) == 8

    @pytest.mark.asyncio
    async def test_confirm_2fa(self, auth_client):
        """Test confirming 2FA setup."""
        expected_payload = {"totp_code": "123456"}
        
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/2fa/confirm", json=expected_payload).respond(200, json={
                "message": "2FA has been successfully enabled"
            })
            
            result = await auth_client.confirm_2fa("123456")
            
            assert result["message"] == "2FA has been successfully enabled"

    @pytest.mark.asyncio
    async def test_disable_2fa(self, auth_client):
        """Test disabling 2FA."""
        expected_payload = {
            "totp_code": "123456",
            "password": "currentpassword"
        }
        
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/2fa/disable", json=expected_payload).respond(200, json={
                "message": "2FA has been successfully disabled"
            })
            
            result = await auth_client.disable_2fa("123456", "currentpassword")
            
            assert result["message"] == "2FA has been successfully disabled"

    @pytest.mark.asyncio
    async def test_get_qr_code(self, auth_client):
        """Test getting QR code image."""
        mock_png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR...'
        
        async with respx.mock(base_url=API_URL) as route:
            route.get("/auth/2fa/qr").respond(200, content=mock_png_data, headers={"Content-Type": "image/png"})
            
            result = await auth_client.get_qr_code()
            
            assert isinstance(result, bytes)
            assert result.startswith(b'\x89PNG')

    @pytest.mark.asyncio
    async def test_request_sms_code(self, auth_client):
        """Test requesting SMS code."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/2fa/request-sms").respond(200, json={
                "message": "SMS code sent successfully", 
                "expires_in": 300
            })
            
            result = await auth_client.request_sms_code()
            
            assert result["message"] == "SMS code sent successfully"
            assert result["expires_in"] == 300


class TestAsyncDebugEndpoints:
    """Test async debug and troubleshooting endpoints."""

    @pytest.mark.asyncio
    async def test_debug_2fa(self, auth_client):
        """Test debug endpoint for TOTP troubleshooting."""
        async with respx.mock(base_url=API_URL) as route:
            route.get("/auth/debug-2fa").respond(200, json={
                "totp_secret_exists": True,
                "user_email": "user@example.com",
                "preferred_2fa_method": "totp",
                "is_2fa_enabled": True,
                "current_server_time": 1720742400,
                "valid_codes": {
                    "time_step_-1": "987654",
                    "time_step_+0": "123456",
                    "time_step_+1": "456789"
                },
                "usage_note": "Try the code for time_step_+0 first, then time_step_-1 or time_step_+1 if needed",
                "message": "Try the code shown for 'time_step_+0' first. If that fails, try the others."
            })
            
            result = await auth_client.debug_2fa()
            
            assert result["totp_secret_exists"] is True
            assert result["user_email"] == "user@example.com"
            assert "123456" in result["valid_codes"]["time_step_+0"]
            assert len(result["valid_codes"]) == 3

    @pytest.mark.asyncio
    async def test_debug_2fa_not_configured(self, auth_client):
        """Test debug endpoint when 2FA is not configured."""
        async with respx.mock(base_url=API_URL) as route:
            route.get("/auth/debug-2fa").respond(400, json={"detail": "TOTP not set up for this user"})
            
            with pytest.raises(httpx.HTTPStatusError):
                await auth_client.debug_2fa()

    @pytest.mark.asyncio
    async def test_refresh_token(self, auth_client):
        """Test token refresh functionality."""
        expected_payload = {"refresh_token": "refresh_token_123"}
        
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/refresh", json=expected_payload).respond(200, json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.refreshed...",
                "token_type": "bearer",
                "expires_in": 1800
            })
            
            result = await auth_client.refresh("refresh_token_123")
            
            assert result["access_token"].startswith("eyJ0eXA")
            assert result["token_type"] == "bearer"
            assert result["expires_in"] == 1800


class TestAsyncErrorHandling:
    """Test various error scenarios and edge cases in async context."""

    @pytest.mark.asyncio
    async def test_network_error_handling(self, auth_client):
        """Test handling of network errors."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/login").side_effect = httpx.ConnectError("Network unreachable")
            
            with pytest.raises(httpx.ConnectError):
                await auth_client.login("user@example.com", "password123")

    @pytest.mark.asyncio
    async def test_server_error_handling(self, auth_client):
        """Test handling of server errors."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/login").respond(500, json={"detail": "Internal server error"})
            
            with pytest.raises(httpx.HTTPStatusError):
                await auth_client.login("user@example.com", "password123")

    @pytest.mark.asyncio
    async def test_timeout_error_handling(self, auth_client):
        """Test handling of timeout errors."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/login").side_effect = httpx.TimeoutException("Request timed out")
            
            with pytest.raises(httpx.TimeoutException):
                await auth_client.login("user@example.com", "password123")

    @pytest.mark.asyncio
    async def test_malformed_json_response(self, auth_client):
        """Test handling of malformed JSON responses."""
        async with respx.mock(base_url=API_URL) as route:
            route.post("/auth/login").respond(200, content=b"not json", headers={"Content-Type": "application/json"})
            
            with pytest.raises(Exception):  # JSON decode error
                await auth_client.login("user@example.com", "password123")


class TestAsyncClientLifecycle:
    """Test async client lifecycle and resource management."""

    @pytest.mark.asyncio
    async def test_client_context_manager(self):
        """Test using async client as context manager."""
        async with httpx.AsyncClient() as http_client:
            auth_client = AsyncAuthClient(http_client, API_URL)
            
            async with respx.mock(base_url=API_URL) as route:
                route.post("/auth/login").respond(200, json={
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "token_type": "bearer"
                })
                
                result = await auth_client.login("user@example.com", "password123")
                assert isinstance(result, Token)

    @pytest.mark.asyncio
    async def test_multiple_concurrent_requests(self):
        """Test making multiple concurrent requests."""
        async with httpx.AsyncClient() as http_client:
            auth_client = AsyncAuthClient(http_client, API_URL)
            
            async with respx.mock(base_url=API_URL) as route:
                route.get("/auth/2fa/status").respond(200, json={
                    "is_2fa_enabled": True,
                    "preferred_2fa_method": "totp",
                    "is_sms_enabled": False
                })
                
                route.get("/auth/debug-2fa").respond(200, json={
                    "totp_secret_exists": True,
                    "user_email": "user@example.com",
                    "valid_codes": {"time_step_+0": "123456"}
                })
                
                # Make concurrent requests
                import asyncio
                results = await asyncio.gather(
                    auth_client.get_2fa_status(),
                    auth_client.debug_2fa(),
                    return_exceptions=True
                )
                
                assert len(results) == 2
                assert isinstance(results[0], TwoFactorStatusResponse)
                assert isinstance(results[1], dict)


# Integration-style tests for realistic workflows
class TestAsyncIntegrationWorkflows:
    """Test realistic end-to-end workflows."""

    @pytest.mark.asyncio
    async def test_complete_user_registration_and_login_workflow(self):
        """Test complete workflow from registration to authenticated API access."""
        async with httpx.AsyncClient() as http_client:
            auth_client = AsyncAuthClient(http_client, API_URL)
            
            async with respx.mock(base_url=API_URL) as route:
                # 1. Register user
                route.post("/auth/register").respond(201, json={
                    "secret": "JBSWY3DPEHPK3PXP",
                    "qr_code_uri": "otpauth://totp/CirtusAI:newuser@example.com?secret=JBSWY3DPEHPK3PXP&issuer=CirtusAI",
                    "qr_code_image": "iVBORw0KGgoAAAANSUhEUgAAAQEAAAEBCAYAAA...",
                    "backup_codes": ["CODE1", "CODE2", "CODE3", "CODE4", "CODE5", "CODE6", "CODE7", "CODE8"]
                })
                
                # 2. Login (2FA required)
                route.post("/auth/login").respond(200, json={
                    "requires_2fa": True,
                    "temporary_token": "temp_token_workflow",
                    "preferred_method": "totp",
                    "message": "2FA verification required."
                })
                
                # 3. Verify 2FA
                route.post("/auth/verify-2fa").respond(200, json={
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.workflow...",
                    "token_type": "bearer"
                })
                
                # Execute workflow
                setup_result = await auth_client.register(
                    username="newuser",
                    email="newuser@example.com",
                    password="SecurePass123!"
                )
                assert isinstance(setup_result, TwoFactorSetupResponse)
                
                login_result = await auth_client.login("newuser@example.com", "SecurePass123!")
                assert isinstance(login_result, TwoFactorRequiredResponse)
                
                final_token = await auth_client.verify_2fa(login_result.temporary_token, "123456")
                assert isinstance(final_token, Token)
                assert final_token.access_token.endswith("workflow...")

    @pytest.mark.asyncio
    async def test_error_recovery_workflow(self, auth_client):
        """Test error recovery scenarios."""
        async with httpx.AsyncClient() as http_client:
            auth_client = AsyncAuthClient(http_client, API_URL)

            # Single mock: first 401 error, then 200 success
            async with respx.mock(base_url=API_URL) as route:
                mock_route = route.post("/auth/verify-2fa")
                mock_route.side_effect = [
                    httpx.Response(401, json={
                        "detail": "Invalid TOTP code '111111'. Valid codes right now: 123456."
                    }),
                    httpx.Response(200, json={
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.recovered...",
                        "token_type": "bearer"
                    })
                ]

                # First attempt should raise our custom error
                with pytest.raises(TwoFactorAuthenticationError) as exc_info:
                    await auth_client.verify_2fa("temp_token", "111111")
                assert "Invalid TOTP code" in str(exc_info.value)

                # Second attempt should succeed
                result = await auth_client.verify_2fa("temp_token", "123456")
                assert isinstance(result, Token)
                assert result.access_token.endswith("recovered...")
