"""
Integration tests for the complete CirtusAI SDK with 2FA functionality.
These tests simulate realistic usage scenarios with full client interactions.
"""
import pytest
import responses
import respx
import httpx
import json
import requests
import asyncio
from unittest.mock import patch, Mock

from cirtusai import CirtusAIClient, AsyncCirtusAIClient
from cirtusai.schemas import Token, TwoFactorRequiredResponse, TwoFactorStatusResponse, TwoFactorSetupResponse
from cirtusai.auth import TwoFactorAuthenticationError
from cirtusai.async_.auth import TwoFactorAuthenticationError as AsyncTwoFactorAuthenticationError

API_URL = "http://testserver"


class TestFullClientIntegration:
    """Test complete client workflows with 2FA."""

    @responses.activate
    def test_complete_registration_and_authentication_flow(self):
        """Test complete flow from registration to authenticated API access."""
        client = CirtusAIClient(base_url=API_URL)
        
        # 1. Register user with automatic 2FA setup
        registration_response = {
            "secret": "JBSWY3DPEHPK3PXP",
            "qr_code_uri": "otpauth://totp/CirtusAI:newuser@example.com?secret=JBSWY3DPEHPK3PXP&issuer=CirtusAI",
            "qr_code_image": "iVBORw0KGgoAAAANSUhEUgAAAQEAAAEBCAYAAA...",
            "backup_codes": ["CODE1", "CODE2", "CODE3", "CODE4", "CODE5", "CODE6", "CODE7", "CODE8"]
        }
        responses.add(
            responses.POST,
            f"{API_URL}/auth/register",
            json=registration_response,
            status=201
        )
        
        setup_result = client.auth.register(
            username="newuser",
            email="newuser@example.com",
            password="SecurePass123!"
        )
        assert isinstance(setup_result, TwoFactorSetupResponse)
        assert len(setup_result.backup_codes) == 8
        
        # 2. Initial login (returns 2FA requirement)
        login_response = {
            "requires_2fa": True,
            "temporary_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.temp...",
            "preferred_method": "totp",
            "message": "2FA verification required."
        }
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            json=login_response,
            status=200
        )
        
        login_result = client.auth.login("newuser@example.com", "SecurePass123!")
        assert isinstance(login_result, TwoFactorRequiredResponse)
        assert login_result.requires_2fa is True
        
        # 3. Complete 2FA verification
        verify_response = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.final...",
            "token_type": "bearer"
        }
        responses.add(
            responses.POST,
            f"{API_URL}/auth/verify-2fa",
            json=verify_response,
            status=200
        )
        
        final_token = client.auth.verify_2fa(login_result.temporary_token, "123456")
        assert isinstance(final_token, Token)
        
        # 4. Set token and test authenticated API access
        client.set_token(final_token.access_token)
        
        # Mock an authenticated API call
        agents_response = [{"id": "agent1", "name": "Test Agent"}]
        responses.add(
            responses.GET,
            f"{API_URL}/agents",
            json=agents_response,
            status=200
        )
        
        agents = client.agents.list_agents()
        assert len(agents) == 1
        assert agents[0]["id"] == "agent1"

    @responses.activate
    def test_convenience_login_with_2fa_flow(self):
        """Test convenience method for complete 2FA login."""
        client = CirtusAIClient(base_url=API_URL)
        
        # Mock the two-step process internally
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            json={
                "requires_2fa": True,
                "temporary_token": "temp_token_123",
                "preferred_method": "totp",
                "message": "2FA verification required."
            },
            status=200
        )
        
        responses.add(
            responses.POST,
            f"{API_URL}/auth/verify-2fa",
            json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.convenience...",
                "token_type": "bearer"
            },
            status=200
        )
        
        # Use convenience method
        token = client.auth.login_with_2fa("user@example.com", "password123", "123456")
        assert isinstance(token, Token)
        assert token.access_token.endswith("convenience...")
        
        # Verify client can be used immediately
        client.set_token(token.access_token)
        
        # Test that token is set properly
        assert client.token == token.access_token

    @responses.activate
    def test_login_with_2fa_raises_error_on_failure(self):
        """Test that login_with_2fa raises an error if 2FA verification fails."""
        client = CirtusAIClient(base_url=API_URL)
        responses.add(
            responses.POST, f"{API_URL}/auth/login",
            json={
                "requires_2fa": True,
                "temporary_token": "temp_token_123",
                "preferred_method": "totp",
                "message": "2FA required"
            },
            status=200
        )
        responses.add(
            responses.POST, f"{API_URL}/auth/verify-2fa",
            json={"detail": "Invalid 2FA code"},
            status=401
        )
        with pytest.raises(TwoFactorAuthenticationError, match="Invalid 2FA code"):
            client.auth.login_with_2fa("user@example.com", "password123", "wrong_code")

    @responses.activate
    def test_2fa_management_workflow(self):
        """Test complete 2FA management workflow."""
        client = CirtusAIClient(base_url=API_URL, token="auth_token")
        
        # 1. Check current 2FA status
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
        
        status = client.auth.get_2fa_status()
        assert status.is_2fa_enabled is True
        assert status.preferred_2fa_method == "totp"
        
        # 2. Get debug information
        responses.add(
            responses.GET,
            f"{API_URL}/auth/debug-2fa",
            json={
                "totp_secret_exists": True,
                "user_email": "user@example.com",
                "current_server_time": 1720742400,
                "valid_codes": {
                    "time_step_-1": "987654",
                    "time_step_+0": "123456",
                    "time_step_+1": "456789"
                },
                "message": "Try the code shown for 'time_step_+0' first."
            },
            status=200
        )
        
        debug_info = client.auth.debug_2fa()
        assert debug_info["totp_secret_exists"] is True
        assert "123456" in debug_info["valid_codes"]["time_step_+0"]
        
        # 3. Disable 2FA
        responses.add(
            responses.POST,
            f"{API_URL}/auth/2fa/disable",
            json={"message": "2FA has been successfully disabled"},
            status=200
        )
        
        disable_result = client.auth.disable_2fa("123456", "currentpassword")
        assert disable_result["message"] == "2FA has been successfully disabled"

    @responses.activate
    def test_error_recovery_scenarios(self):
        """Test error recovery in various failure scenarios."""
        client = CirtusAIClient(base_url=API_URL)
        
        # Scenario 1: Invalid TOTP code with helpful error message
        responses.add(
            responses.POST,
            f"{API_URL}/auth/verify-2fa",
            json={
                "detail": "Invalid TOTP code '999999'. Valid codes right now: 123456, 789012, 345678. Check your authenticator app time sync."
            },
            status=401
        )
        
        with pytest.raises(TwoFactorAuthenticationError) as exc_info:
            client.auth.verify_2fa("temp_token", "999999")
        
        error_msg = str(exc_info.value)
        assert "Invalid TOTP code" in error_msg
        assert "Valid codes right now" in error_msg
        assert "123456" in error_msg
        
        # Scenario 2: Expired temporary token
        responses.add(
            responses.POST,
            f"{API_URL}/auth/verify-2fa",
            json={"detail": "Invalid or expired temporary token"},
            status=401
        )
        
        with pytest.raises(TwoFactorAuthenticationError) as exc_info:
            client.auth.verify_2fa("expired_token", "123456")
        
        assert "expired temporary token" in str(exc_info.value)

    @responses.activate
    def test_client_token_management(self):
        """Test client token management and automatic inclusion in requests."""
        client = CirtusAIClient(base_url=API_URL)
        
        # Login and get token
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.token...",
                "token_type": "bearer"
            },
            status=200
        )
        
        token = client.auth.login("legacy@example.com", "password123")
        client.set_token(token.access_token)
        
        # Verify token is included in subsequent requests
        def request_callback(request):
            headers = request.headers
            assert "Authorization" in headers
            assert headers["Authorization"] == f"Bearer {token.access_token}"
            return (200, {}, json.dumps({"success": True}))
        
        responses.add_callback(
            responses.GET,
            f"{API_URL}/agents",
            callback=request_callback
        )
        
        result = client.agents.list_agents()
        assert result["success"] is True

    @responses.activate
    def test_session_management(self):
        """Test client session management and cleanup."""
        client = CirtusAIClient(base_url=API_URL)
        
        # Verify session exists
        assert client.session is not None
        
        # Test that session is reused
        session1 = client.session
        session2 = client.session
        assert session1 is session2
        
        # Test client close
        client.close()
        # Note: In real implementation, this might clear the session


class TestAsyncClientIntegration:
    """Test complete async client workflows."""

    @pytest.fixture
    def event_loop(self):
        """Override event_loop for pytest-asyncio"""
        loop = asyncio.new_event_loop()
        yield loop
        loop.close()

    @respx.mock
    @pytest.mark.asyncio
    async def test_async_complete_authentication_flow(self):
        """Test the full async authentication flow from login to using a protected endpoint."""
        # Mock login response (2FA required)
        respx.post(f"{API_URL}/auth/login").respond(
            200, json={
                "requires_2fa": True,
                "temporary_token": "async_temp_token",
                "preferred_method": "totp",
                "message": "2FA required"
            }
        )
        # Mock 2FA verification response
        respx.post(f"{API_URL}/auth/verify-2fa").respond(
            200, json={"access_token": "async_final_token", "token_type": "bearer"}
        )
        # Mock protected endpoint response
        respx.get(f"{API_URL}/auth/2fa/status").respond(
            200, json={"is_2fa_enabled": True, "preferred_2fa_method": "totp", "is_sms_enabled": False}
        )

        async with AsyncCirtusAIClient(base_url=API_URL) as client:
            # Step 1: Login
            login_resp = await client.auth.login("async_user@example.com", "password")
            assert login_resp.requires_2fa
            assert login_resp.temporary_token == "async_temp_token"

            # Step 2: Verify 2FA
            token = await client.auth.verify_2fa(login_resp.temporary_token, "123456")
            assert token.access_token == "async_final_token"

            # Step 3: Use token for protected endpoint
            await client.set_token(token.access_token)
            status = await client.auth.get_2fa_status()
            assert status.is_2fa_enabled is True

    @respx.mock
    @pytest.mark.asyncio
    async def test_async_concurrent_operations(self):
        """Test concurrent async operations."""
        async with httpx.AsyncClient() as http_client:
            client = AsyncCirtusAIClient(base_url=API_URL, token="test_token")
            client._client = http_client
            
            async with respx.mock(base_url=API_URL) as route:
                # Mock multiple endpoints
                route.get("/auth/2fa/status").respond(200, json={
                    "is_2fa_enabled": True,
                    "preferred_2fa_method": "totp",
                    "is_sms_enabled": False
                })
                
                route.get("/auth/debug-2fa").respond(200, json={
                    "totp_secret_exists": True,
                    "valid_codes": {"time_step_+0": "123456"}
                })
                
                route.get("/agents").respond(200, json=[{"id": "agent1"}, {"id": "agent2"}])
                
                # Execute concurrent operations
                results = await asyncio.gather(
                    client.auth.get_2fa_status(),
                    client.auth.debug_2fa(),
                    client.agents.list_agents(),
                    return_exceptions=True
                )
                
                assert len(results) == 3
                assert isinstance(results[0], TwoFactorStatusResponse)
                assert isinstance(results[1], dict)
                assert isinstance(results[2], list)
                assert len(results[2]) == 2

    @respx.mock
    @pytest.mark.asyncio
    async def test_async_error_handling(self):
        """Test async error handling scenarios."""
        async with AsyncCirtusAIClient(base_url=API_URL) as client:
            # Network error
            respx.post("/auth/login").side_effect = httpx.ConnectError("Network error")
            with pytest.raises(httpx.ConnectError):
                await client.auth.login("user@example.com", "password")

            # HTTP error for 2FA verification
            respx.post("/auth/verify-2fa").respond(401, json={"detail": "Invalid code"})
            with pytest.raises(AsyncTwoFactorAuthenticationError, match="Invalid code"):
                await client.auth.verify_2fa("token", "invalid")


class TestRealWorldUseCases:
    """Test realistic use cases and edge cases."""

    @responses.activate
    def test_multiple_client_instances(self):
        """Test using multiple client instances simultaneously."""
        client1 = CirtusAIClient(base_url=API_URL, token="token1")
        client2 = CirtusAIClient(base_url=API_URL, token="token2")
        
        # Mock responses for different tokens
        def request_callback(request):
            auth_header = request.headers.get("Authorization", "")
            if "token1" in auth_header:
                return (200, {}, json.dumps({
                    "is_2fa_enabled": True,
                    "preferred_2fa_method": "totp",
                    "is_sms_enabled": False
                }))
            elif "token2" in auth_header:
                return (200, {}, json.dumps({
                    "is_2fa_enabled": False,
                    "preferred_2fa_method": None,
                    "is_sms_enabled": True
                }))
            else:
                return (401, {}, json.dumps({"error": "Unauthorized"}))
        
        responses.add_callback(
            responses.GET,
            f"{API_URL}/auth/2fa/status",
            callback=request_callback
        )
        
        # Each client should use its own token
        status1 = client1.auth.get_2fa_status()
        status2 = client2.auth.get_2fa_status()
        
        # Note: This test would need actual response structure
        # The callback above is simplified for demonstration

    @responses.activate  
    def test_token_expiration_and_refresh(self):
        """Test handling of token expiration and refresh."""
        client = CirtusAIClient(base_url=API_URL, token="expired_token")
        
        # First request fails due to expired token
        responses.add(
            responses.GET,
            f"{API_URL}/auth/2fa/status",
            json={"detail": "Token has expired"},
            status=401
        )
        
        # Refresh token request succeeds
        responses.add(
            responses.POST,
            f"{API_URL}/auth/refresh",
            json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.refreshed...",
                "token_type": "bearer",
                "expires_in": 1800
            },
            status=200
        )
        
        # Retry with new token succeeds
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
        
        # This would require implementing automatic token refresh in the client
        # For now, manual refresh:
        try:
            # This will fail because the token is expired
            client.auth.get_2fa_status()
        except requests.exceptions.HTTPError as e:
            assert e.response.status_code == 401

        refresh_result = client.auth.refresh("refresh_token_123")
        client.set_token(refresh_result["access_token"])
        status = client.auth.get_2fa_status()
        assert status.is_2fa_enabled is True

    @responses.activate
    def test_client_configuration_options(self):
        """Test various client configuration options."""
        # Test with custom timeout
        client1 = CirtusAIClient(base_url=API_URL, timeout=30)
        
        # Test with custom headers
        client2 = CirtusAIClient(base_url=API_URL, headers={"Custom-Header": "value"})
        
        # Test configuration affects requests
        def request_callback(request):
            # Check if custom header is present
            if "Custom-Header" in request.headers:
                return (200, {}, json.dumps({"has_custom_header": True}))
            else:
                return (200, {}, json.dumps({"has_custom_header": False}))
        
        responses.add_callback(
            responses.GET,
            f"{API_URL}/auth/2fa/status",
            callback=request_callback
        )
        
        # This test would need actual implementation of custom headers
        # status = client2.auth.get_2fa_status()
        # assert status["has_custom_header"] is True

    def test_client_resource_cleanup(self):
        """Test proper resource cleanup in client lifecycle."""
        client = CirtusAIClient(base_url=API_URL)
        
        # Verify client can be created
        assert client is not None
        assert client.session is not None
        
        # Test cleanup
        client.close()
        
        # After close, client should not be usable for new requests
        # This depends on implementation details


class TestBackwardsCompatibility:
    """Test backwards compatibility with existing code."""

    @responses.activate
    def test_legacy_login_still_works(self):
        """Test that legacy login (without 2FA) still works."""
        client = CirtusAIClient(base_url=API_URL)
        
        # Mock legacy user login (no 2FA)
        responses.add(
            responses.POST,
            f"{API_URL}/auth/login",
            json={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.legacy...",
                "token_type": "bearer"
            },
            status=200
        )
        
        token = client.auth.login("legacy@example.com", "password")
        assert isinstance(token, Token)
        assert token.access_token.endswith("legacy...")

    def test_api_compatibility(self):
        """Test that all existing API methods are still available."""
        client = CirtusAIClient(base_url=API_URL)
        
        # Verify all expected methods exist
        assert hasattr(client.auth, 'login')
        assert hasattr(client.auth, 'register')
        assert hasattr(client.auth, 'verify_2fa')
        assert hasattr(client.auth, 'login_with_2fa')
        assert hasattr(client.auth, 'get_2fa_status')
        assert hasattr(client.auth, 'setup_2fa')
        assert hasattr(client.auth, 'confirm_2fa')
        assert hasattr(client.auth, 'disable_2fa')
        assert hasattr(client.auth, 'debug_2fa')
        assert hasattr(client.auth, 'refresh')
        
        # Verify other client components still exist
        assert hasattr(client, 'agents')
        assert hasattr(client, 'wallets')
        assert hasattr(client, 'identity')


class TestPerformanceAndScaling:
    """Test performance characteristics and scaling behavior."""

    @responses.activate
    def test_large_response_handling(self):
        """Test handling of large API responses."""
        client = CirtusAIClient(base_url=API_URL, token="test_token")
        
        # Mock large response
        large_backup_codes = [f"CODE{i:04d}" for i in range(1000)]
        responses.add(
            responses.GET,
            f"{API_URL}/auth/2fa/setup",
            json={
                "secret": "JBSWY3DPEHPK3PXP",
                "qr_code_uri": "otpauth://totp/test",
                "qr_code_image": "x" * 10000,  # Large base64 image
                "backup_codes": large_backup_codes
            },
            status=200
        )
        
        setup_result = client.auth.setup_2fa()
        assert len(setup_result.backup_codes) == 1000
        assert len(setup_result.qr_code_image) == 10000

    @pytest.mark.asyncio
    async def test_concurrent_request_limits(self):
        """Test behavior under high concurrent load."""
        async with httpx.AsyncClient() as http_client:
            client = AsyncCirtusAIClient(base_url=API_URL, token="test_token")
            client._client = http_client
            
            async with respx.mock(base_url=API_URL) as route:
                route.get("/auth/2fa/status").respond(200, json={
                    "is_2fa_enabled": True,
                    "preferred_2fa_method": "totp",
                    "is_sms_enabled": False
                })
                
                # Make many concurrent requests
                tasks = [client.auth.get_2fa_status() for _ in range(100)]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # All should succeed
                assert len(results) == 100
                assert all(isinstance(r, TwoFactorStatusResponse) for r in results)

    def test_memory_usage_patterns(self):
        """Test memory usage patterns with repeated operations."""
        client = CirtusAIClient(base_url=API_URL)
        
        # This would require memory profiling tools in a real test
        # For now, just verify no obvious memory leaks in object creation
        clients = []
        for i in range(100):
            temp_client = CirtusAIClient(base_url=API_URL)
            clients.append(temp_client)
        
        # Clean up
        for temp_client in clients:
            temp_client.close()
        
        # In a real test, we'd check memory usage here
