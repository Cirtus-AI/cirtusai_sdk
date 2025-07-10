"""
Tests for the AuthClient (sync) with comprehensive 2FA functionality.
"""
import pytest
import responses
from requests.exceptions import HTTPError
from responses.matchers import json_params_matcher

from cirtusai.auth import AuthClient, TwoFactorAuthenticationError
from cirtusai.schemas import (
    Token, 
    TwoFactorRequiredResponse, 
    TwoFactorSetupResponse,
    TwoFactorStatusResponse,
    UserRegister,
    TwoFactorVerifyRequest,
    TwoFactorDisableRequest
)
import requests

API_URL = "http://testserver"

@pytest.fixture
def auth_client():
    session = requests.Session()
    return AuthClient(session, API_URL)

class TestUserRegistration:
    """Test user registration with automatic 2FA setup."""
    
    @responses.activate
    def test_register_user_success(self, auth_client):
        """Test successful user registration with 2FA setup."""
        # Expected request payload
        expected_payload = {
            "username": "testuser",
            "email": "test@example.com", 
            "password": "SecurePass123!",
            "preferred_2fa_method": "totp"
        }
        
        # Mock response data
        response_data = {
            "secret": "JBSWY3DPEHPK3PXP",
            "qr_code_uri": "otpauth://totp/CirtusAI:test@example.com?secret=JBSWY3DPEHPK3PXP&issuer=CirtusAI",
            "qr_code_image": "iVBORw0KGgoAAAANSUhEUgAAAQEAAAEBCAYAAA...",
            "backup_codes": ["ABCD1234", "EFGH5678", "IJKL9012", "MNOP3456", "QRST7890", "UVWX1234", "YZAB5678", "CDEF9012"]
        }
        
        responses.add(
            responses.POST,
            f"{API_URL}/auth/register",
            json=response_data,
            status=201,
            match=[json_params_matcher(expected_payload)]
        )
        
        result = auth_client.register(
            username="testuser",
            email="test@example.com",
            password="SecurePass123!",
            preferred_2fa_method="totp"
        )
        
        assert isinstance(result, TwoFactorSetupResponse)
        assert result.secret == "JBSWY3DPEHPK3PXP"
        assert "CirtusAI" in result.qr_code_uri
        assert len(result.backup_codes) == 8
        assert result.qr_code_image.startswith("iVBORw0KGgo")

    @responses.activate
    def test_register_user_default_2fa_method(self, auth_client):
        """Test registration with default 2FA method."""
        expected_payload = {
            "username": "testuser",
            "email": "test@example.com", 
            "password": "SecurePass123!",
            "preferred_2fa_method": "totp"  # Default should be totp
        }
        
        response_data = {
            "secret": "JBSWY3DPEHPK3PXP",
            "qr_code_uri": "otpauth://totp/CirtusAI:test@example.com?secret=JBSWY3DPEHPK3PXP&issuer=CirtusAI",
            "qr_code_image": "iVBORw0KGgoAAAANSUhEUgAAAQEAAAEBCAYAAA...",
            "backup_codes": ["ABCD1234", "EFGH5678"]
        }
        
        responses.add(
            responses.POST,
            f"{API_URL}/auth/register",
            json=response_data,
            status=201,
            match=[json_params_matcher(expected_payload)]
        )
        
        # Don't specify preferred_2fa_method - should default to "totp"
        result = auth_client.register(
            username="testuser",
            email="test@example.com",
            password="SecurePass123!"
        )
        
        assert isinstance(result, TwoFactorSetupResponse)

    @responses.activate
    def test_register_user_username_taken(self, auth_client):
        """Test registration failure when username is taken."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/register",
            json={"detail": "Username already registered"},
            status=400
        )
        
        with pytest.raises(HTTPError):
            auth_client.register(
                username="taken_username",
                email="test@example.com",
                password="SecurePass123!"
            )

    @responses.activate
    def test_register_user_email_taken(self, auth_client):
        """Test registration failure when email is taken.""" 
        responses.add(
            responses.POST,
            f"{API_URL}/auth/register",
            json={"detail": "Email already registered"},
            status=400
        )
        
        with pytest.raises(HTTPError):
            auth_client.register(
                username="testuser",
                email="taken@example.com",
                password="SecurePass123!"
            )


class TestLoginFlow:
    """Test various login scenarios including 2FA flows."""

    @responses.activate
    def test_login_without_2fa(self, auth_client):
        """Test login for legacy user without 2FA enabled."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer"
            },
            status=200
        )
        
        result = auth_client.login("user@example.com", "password123")
        
        assert isinstance(result, Token)
        assert result.access_token.startswith("eyJ0eXA")
        assert result.token_type == "bearer"

    @responses.activate
    def test_login_with_2fa_required(self, auth_client):
        """Test login that requires 2FA verification."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            json={
                "requires_2fa": True,
                "temporary_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.temp...",
                "preferred_method": "totp",
                "message": "2FA verification required. Use the temporary token in /auth/verify-2fa endpoint."
            },
            status=200
        )
        
        result = auth_client.login("user@example.com", "password123")
        
        assert isinstance(result, TwoFactorRequiredResponse)
        assert result.requires_2fa is True
        assert result.temporary_token.startswith("eyJ0eXA")
        assert result.preferred_method == "totp"
        assert "verify-2fa" in result.message

    @responses.activate
    def test_login_invalid_credentials(self, auth_client):
        """Test login with invalid credentials."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            json={"detail": "Incorrect username/email or password"},
            status=401
        )
        
        with pytest.raises(HTTPError):
            auth_client.login("wrong@example.com", "wrongpassword")


class TestTwoFactorVerification:
    """Test 2FA verification flows."""

    @responses.activate
    def test_verify_2fa_success(self, auth_client):
        """Test successful 2FA verification."""
        expected_payload = {
            "temporary_token": "temp_token_123",
            "totp_code": "123456"
        }
        
        responses.add(
            responses.POST,
            f"{API_URL}/auth/verify-2fa",
            json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.final...",
                "token_type": "bearer"
            },
            status=200,
            match=[json_params_matcher(expected_payload)]
        )
        
        result = auth_client.verify_2fa("temp_token_123", "123456")
        
        assert isinstance(result, Token)
        assert result.access_token.startswith("eyJ0eXA")
        assert result.token_type == "bearer"

    @responses.activate
    def test_verify_2fa_invalid_code(self, auth_client):
        """Test 2FA verification with invalid TOTP code."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/verify-2fa",
            json={"detail": "Invalid TOTP code '999999'. Valid codes right now: 123456, 789012, 345678. Check your authenticator app time sync."},
            status=401
        )
        
        with pytest.raises(TwoFactorAuthenticationError) as exc_info:
            auth_client.verify_2fa("temp_token_123", "999999")
        
        assert "Invalid TOTP code" in str(exc_info.value)
        assert "Valid codes right now" in str(exc_info.value)

    @responses.activate 
    def test_verify_2fa_expired_token(self, auth_client):
        """Test 2FA verification with expired temporary token."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/verify-2fa",
            json={"detail": "Invalid or expired temporary token"},
            status=401
        )
        
        with pytest.raises(TwoFactorAuthenticationError) as exc_info:
            auth_client.verify_2fa("expired_token", "123456")
        
        assert "expired temporary token" in str(exc_info.value)


class TestConvenienceMethods:
    """Test convenience methods for complete login flows."""

    @responses.activate
    def test_login_with_2fa_complete_flow(self, auth_client):
        """Test complete login flow with 2FA using convenience method."""
        # First call to login - returns 2FA requirement
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            json={
                "requires_2fa": True,
                "temporary_token": "temp_token_abc",
                "preferred_method": "totp",
                "message": "2FA verification required."
            },
            status=200
        )
        
        # Second call to verify-2fa - returns final token
        responses.add(
            responses.POST,
            f"{API_URL}/auth/verify-2fa",
            json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.final...",
                "token_type": "bearer"
            },
            status=200
        )
        
        result = auth_client.login_with_2fa("user@example.com", "password123", "123456")
        
        assert isinstance(result, Token)
        assert result.access_token.startswith("eyJ0eXA")

    @responses.activate
    def test_login_with_2fa_no_2fa_required(self, auth_client):
        """Test convenience method when 2FA is not required."""
        # Login returns token directly (legacy user)
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.direct...",
                "token_type": "bearer"
            },
            status=200
        )
        
        result = auth_client.login_with_2fa("legacy@example.com", "password123", "123456")
        
        assert isinstance(result, Token)
        assert result.access_token.startswith("eyJ0eXA")

    @responses.activate
    def test_login_with_2fa_verification_fails(self, auth_client):
        """Test convenience method when 2FA verification fails."""
        # First call succeeds
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            json={
                "requires_2fa": True,
                "temporary_token": "temp_token_abc",
                "preferred_method": "totp",
                "message": "2FA verification required."
            },
            status=200
        )
        
        # Second call fails
        responses.add(
            responses.POST,
            f"{API_URL}/auth/verify-2fa",
            json={"detail": "Invalid TOTP code '999999'"},
            status=401
        )
        
        with pytest.raises(TwoFactorAuthenticationError):
            auth_client.login_with_2fa("user@example.com", "password123", "999999")


class TestTwoFactorManagement:
    """Test 2FA management endpoints."""

    @responses.activate
    def test_get_2fa_status(self, auth_client):
        """Test getting 2FA status for authenticated user."""
        responses.add(
            responses.GET,
            f"{API_URL}/auth/2fa/status",
            json={
                "is_2fa_enabled": True,
                "preferred_2fa_method": "totp",
                "is_sms_enabled": False
            },
            status=200
        )
        
        result = auth_client.get_2fa_status()
        
        assert isinstance(result, TwoFactorStatusResponse)
        assert result.is_2fa_enabled is True
        assert result.preferred_2fa_method == "totp"
        assert result.is_sms_enabled is False

    @responses.activate
    def test_setup_2fa(self, auth_client):
        """Test setting up 2FA for existing user."""
        responses.add(
            responses.GET,
            f"{API_URL}/auth/2fa/setup",
            json={
                "secret": "JBSWY3DPEHPK3PXP",
                "qr_code_uri": "otpauth://totp/CirtusAI:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=CirtusAI",
                "qr_code_image": "iVBORw0KGgoAAAANSUhEUgAAAQEAAAEBCAYAAA...",
                "backup_codes": ["CODE1", "CODE2", "CODE3", "CODE4", "CODE5", "CODE6", "CODE7", "CODE8"]
            },
            status=200
        )
        
        result = auth_client.setup_2fa()
        
        assert isinstance(result, TwoFactorSetupResponse)
        assert result.secret == "JBSWY3DPEHPK3PXP"
        assert len(result.backup_codes) == 8

    @responses.activate
    def test_confirm_2fa(self, auth_client):
        """Test confirming 2FA setup."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/2fa/confirm",
            json={"message": "2FA has been successfully enabled"},
            status=200,
            match=[json_params_matcher({"totp_code": "123456"})]
        )
        
        result = auth_client.confirm_2fa("123456")
        
        assert result["message"] == "2FA has been successfully enabled"

    @responses.activate
    def test_disable_2fa(self, auth_client):
        """Test disabling 2FA."""
        expected_payload = {
            "totp_code": "123456",
            "password": "currentpassword"
        }
        
        responses.add(
            responses.POST,
            f"{API_URL}/auth/2fa/disable",
            json={"message": "2FA has been successfully disabled"},
            status=200,
            match=[json_params_matcher(expected_payload)]
        )
        
        result = auth_client.disable_2fa("123456", "currentpassword")
        
        assert result["message"] == "2FA has been successfully disabled"

    @responses.activate
    def test_get_qr_code(self, auth_client):
        """Test getting QR code image."""
        mock_png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR...'
        
        responses.add(
            responses.GET,
            f"{API_URL}/auth/2fa/qr",
            body=mock_png_data,
            status=200,
            headers={"Content-Type": "image/png"}
        )
        
        result = auth_client.get_qr_code()
        
        assert isinstance(result, bytes)
        assert result.startswith(b'\x89PNG')

    @responses.activate
    def test_request_sms_code(self, auth_client):
        """Test requesting SMS code."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/2fa/request-sms",
            json={"message": "SMS code sent successfully", "expires_in": 300},
            status=200
        )
        
        result = auth_client.request_sms_code()
        
        assert result["message"] == "SMS code sent successfully"
        assert result["expires_in"] == 300


class TestDebugEndpoints:
    """Test debug and troubleshooting endpoints."""

    @responses.activate
    def test_debug_2fa(self, auth_client):
        """Test debug endpoint for TOTP troubleshooting."""
        responses.add(
            responses.GET,
            f"{API_URL}/auth/debug-2fa",
            json={
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
            },
            status=200
        )
        
        result = auth_client.debug_2fa()
        
        assert result["totp_secret_exists"] is True
        assert result["user_email"] == "user@example.com"
        assert "123456" in result["valid_codes"]["time_step_+0"]
        assert len(result["valid_codes"]) == 3

    @responses.activate
    def test_debug_2fa_not_configured(self, auth_client):
        """Test debug endpoint when 2FA is not configured."""
        responses.add(
            responses.GET,
            f"{API_URL}/auth/debug-2fa",
            json={"detail": "TOTP not set up for this user"},
            status=400
        )
        
        with pytest.raises(HTTPError):
            auth_client.debug_2fa()

    @responses.activate
    def test_refresh_token(self, auth_client):
        """Test token refresh functionality."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/refresh",
            json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.refreshed...",
                "token_type": "bearer",
                "expires_in": 1800
            },
            status=200,
            match=[json_params_matcher({"refresh_token": "refresh_token_123"})]
        )
        
        result = auth_client.refresh("refresh_token_123")
        
        assert result["access_token"].startswith("eyJ0eXA")
        assert result["token_type"] == "bearer"
        assert result["expires_in"] == 1800


class TestErrorHandling:
    """Test various error scenarios and edge cases."""

    @responses.activate
    def test_network_error_handling(self, auth_client):
        """Test handling of network errors."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            body=responses.ConnectionError("Network unreachable")
        )
        
        with pytest.raises(responses.ConnectionError):
            auth_client.login("user@example.com", "password123")

    @responses.activate
    def test_server_error_handling(self, auth_client):
        """Test handling of server errors."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            json={"detail": "Internal server error"},
            status=500
        )
        
        with pytest.raises(HTTPError):
            auth_client.login("user@example.com", "password123")

    @responses.activate
    def test_malformed_response_handling(self, auth_client):
        """Test handling of malformed responses."""
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            body="not json",
            status=200,
            headers={"Content-Type": "application/json"}
        )
        
        with pytest.raises(Exception):  # JSON decode error
            auth_client.login("user@example.com", "password123")
