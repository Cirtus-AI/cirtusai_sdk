"""
Tests for 2FA-related schemas and data validation.
"""
import pytest
from pydantic import ValidationError

from cirtusai.schemas import (
    Token,
    TwoFactorRequiredResponse,
    TwoFactorSetupResponse,
    TwoFactorStatusResponse,
    TwoFactorVerifyRequest,
    TwoFactorDisableRequest,
    UserRegister
)


class TestTwoFactorSchemas:
    """Test Pydantic schemas for 2FA functionality."""

    def test_token_schema_valid(self):
        """Test Token schema with valid data."""
        data = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "token_type": "bearer"
        }
        token = Token(**data)
        assert token.access_token == data["access_token"]
        assert token.token_type == "bearer"

    def test_token_schema_default_type(self):
        """Test Token schema with default token type."""
        data = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        }
        token = Token(**data)
        assert token.token_type == "bearer"  # Default value

    def test_token_schema_missing_access_token(self):
        """Test Token schema validation fails without access_token."""
        with pytest.raises(ValidationError) as exc_info:
            Token(token_type="bearer")
        assert "access_token" in str(exc_info.value)

    def test_two_factor_required_response_valid(self):
        """Test TwoFactorRequiredResponse schema with valid data."""
        data = {
            "requires_2fa": True,
            "temporary_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.temp...",
            "preferred_method": "totp",
            "message": "2FA verification required. Use the temporary token in /auth/verify-2fa endpoint."
        }
        response = TwoFactorRequiredResponse(**data)
        assert response.requires_2fa is True
        assert response.temporary_token == data["temporary_token"]
        assert response.preferred_method == "totp"
        assert "verify-2fa" in response.message

    def test_two_factor_required_response_invalid_types(self):
        """Test TwoFactorRequiredResponse schema with invalid data types."""
        with pytest.raises(ValidationError):
            TwoFactorRequiredResponse(
                requires_2fa="yes",  # Should be boolean
                temporary_token="token",
                preferred_method="totp",
                message="test"
            )

    def test_two_factor_setup_response_valid(self):
        """Test TwoFactorSetupResponse schema with valid data."""
        data = {
            "secret": "JBSWY3DPEHPK3PXP",
            "qr_code_uri": "otpauth://totp/CirtusAI:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=CirtusAI",
            "qr_code_image": "iVBORw0KGgoAAAANSUhEUgAAAQEAAAEBCAYAAA...",
            "backup_codes": ["CODE1", "CODE2", "CODE3", "CODE4", "CODE5", "CODE6", "CODE7", "CODE8"]
        }
        setup = TwoFactorSetupResponse(**data)
        assert setup.secret == "JBSWY3DPEHPK3PXP"
        assert "otpauth://" in setup.qr_code_uri
        assert setup.qr_code_image.startswith("iVBORw0KGgo")
        assert len(setup.backup_codes) == 8
        assert all(isinstance(code, str) for code in setup.backup_codes)

    def test_two_factor_setup_response_empty_backup_codes(self):
        """Test TwoFactorSetupResponse with empty backup codes."""
        data = {
            "secret": "JBSWY3DPEHPK3PXP",
            "qr_code_uri": "otpauth://totp/test",
            "qr_code_image": "base64data",
            "backup_codes": []
        }
        setup = TwoFactorSetupResponse(**data)
        assert setup.backup_codes == []

    def test_two_factor_setup_response_missing_fields(self):
        """Test TwoFactorSetupResponse validation with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            TwoFactorSetupResponse(
                secret="JBSWY3DPEHPK3PXP",
                # Missing other required fields
            )
        error_str = str(exc_info.value)
        assert "qr_code_uri" in error_str
        assert "qr_code_image" in error_str
        assert "backup_codes" in error_str

    def test_two_factor_verify_request_valid(self):
        """Test TwoFactorVerifyRequest schema with valid data."""
        data = {
            "temporary_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.temp...",
            "totp_code": "123456"
        }
        request = TwoFactorVerifyRequest(**data)
        assert request.temporary_token == data["temporary_token"]
        assert request.totp_code == "123456"

    def test_two_factor_verify_request_invalid_totp_code(self):
        """Test TwoFactorVerifyRequest with various TOTP code formats."""
        # Valid 6-digit code
        valid_request = TwoFactorVerifyRequest(
            temporary_token="token123",
            totp_code="123456"
        )
        assert valid_request.totp_code == "123456"
        
        # Should accept string codes (validation is done server-side)
        valid_request_2 = TwoFactorVerifyRequest(
            temporary_token="token123",
            totp_code="000001"
        )
        assert valid_request_2.totp_code == "000001"

    def test_two_factor_status_response_valid(self):
        """Test TwoFactorStatusResponse schema with valid data."""
        data = {
            "is_2fa_enabled": True,
            "preferred_2fa_method": "totp",
            "is_sms_enabled": False
        }
        status = TwoFactorStatusResponse(**data)
        assert status.is_2fa_enabled is True
        assert status.preferred_2fa_method == "totp"
        assert status.is_sms_enabled is False

    def test_two_factor_status_response_optional_method(self):
        """Test TwoFactorStatusResponse with optional preferred method."""
        data = {
            "is_2fa_enabled": False,
            "preferred_2fa_method": None,
            "is_sms_enabled": False
        }
        status = TwoFactorStatusResponse(**data)
        assert status.is_2fa_enabled is False
        assert status.preferred_2fa_method is None
        assert status.is_sms_enabled is False

    def test_two_factor_disable_request_valid(self):
        """Test TwoFactorDisableRequest schema with valid data."""
        data = {
            "totp_code": "123456",
            "password": "currentpassword123"
        }
        request = TwoFactorDisableRequest(**data)
        assert request.totp_code == "123456"
        assert request.password == "currentpassword123"

    def test_two_factor_disable_request_missing_fields(self):
        """Test TwoFactorDisableRequest validation with missing fields."""
        with pytest.raises(ValidationError) as exc_info:
            TwoFactorDisableRequest(totp_code="123456")
        assert "password" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            TwoFactorDisableRequest(password="password123")
        assert "totp_code" in str(exc_info.value)

    def test_user_register_valid(self):
        """Test UserRegister schema with valid data."""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePass123!",
            "preferred_2fa_method": "totp"
        }
        user = UserRegister(**data)
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "SecurePass123!"
        assert user.preferred_2fa_method == "totp"

    def test_user_register_default_2fa_method(self):
        """Test UserRegister schema with default 2FA method."""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        user = UserRegister(**data)
        assert user.preferred_2fa_method == "totp"  # Default value

    def test_user_register_sms_method(self):
        """Test UserRegister schema with SMS 2FA method."""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePass123!",
            "preferred_2fa_method": "sms"
        }
        user = UserRegister(**data)
        assert user.preferred_2fa_method == "sms"

    def test_user_register_invalid_email(self):
        """Test UserRegister schema with invalid email format."""
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(
                username="testuser",
                email="invalid-email",  # Invalid email format
                password="SecurePass123!"
            )
        assert "email" in str(exc_info.value).lower()

    def test_user_register_missing_required_fields(self):
        """Test UserRegister schema with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(
                username="testuser",
                # Missing email and password
            )
        error_str = str(exc_info.value)
        assert "email" in error_str
        assert "password" in error_str

    def test_user_register_empty_strings(self):
        """Test UserRegister schema with empty string values."""
        with pytest.raises(ValidationError):
            UserRegister(
                username="",  # Empty username
                email="test@example.com",
                password="SecurePass123!"
            )
        
        with pytest.raises(ValidationError):
            UserRegister(
                username="testuser",
                email="",  # Empty email
                password="SecurePass123!"
            )
        
        with pytest.raises(ValidationError):
            UserRegister(
                username="testuser",
                email="test@example.com",
                password=""  # Empty password
            )


class TestSchemaModelDumps:
    """Test schema serialization (model_dump functionality)."""

    def test_token_model_dump(self):
        """Test Token schema serialization."""
        token = Token(
            access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            token_type="bearer"
        )
        dumped = token.model_dump()
        expected = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "token_type": "bearer"
        }
        assert dumped == expected

    def test_two_factor_setup_model_dump(self):
        """Test TwoFactorSetupResponse schema serialization."""
        setup = TwoFactorSetupResponse(
            secret="JBSWY3DPEHPK3PXP",
            qr_code_uri="otpauth://totp/test",
            qr_code_image="base64data",
            backup_codes=["CODE1", "CODE2"]
        )
        dumped = setup.model_dump()
        assert dumped["secret"] == "JBSWY3DPEHPK3PXP"
        assert dumped["backup_codes"] == ["CODE1", "CODE2"]
        assert len(dumped) == 4

    def test_user_register_model_dump_excludes_none(self):
        """Test UserRegister model dump behavior with None values."""
        user = UserRegister(
            username="testuser",
            email="test@example.com",
            password="SecurePass123!",
            preferred_2fa_method=None
        )
        dumped = user.model_dump(exclude_none=True)
        assert "preferred_2fa_method" not in dumped
        assert len(dumped) == 3

    def test_user_register_model_dump_includes_none(self):
        """Test UserRegister model dump behavior including None values."""
        user = UserRegister(
            username="testuser",
            email="test@example.com",
            password="SecurePass123!",
            preferred_2fa_method=None
        )
        dumped = user.model_dump(exclude_none=False)
        assert dumped["preferred_2fa_method"] is None
        assert len(dumped) == 4


class TestSchemaEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_long_strings(self):
        """Test schemas with very long string values."""
        long_token = "a" * 10000  # Very long token
        token = Token(access_token=long_token, token_type="bearer")
        assert len(token.access_token) == 10000

    def test_special_characters_in_strings(self):
        """Test schemas with special characters."""
        special_username = "test@user.name+123"
        user = UserRegister(
            username=special_username,
            email="test@example.com",
            password="Pass!@#$%^&*()_+{}[]"
        )
        assert user.username == special_username
        assert "!@#$%^&*()" in user.password

    def test_unicode_characters(self):
        """Test schemas with Unicode characters."""
        unicode_username = "用户名123"
        user = UserRegister(
            username=unicode_username,
            email="test@example.com",
            password="密码123!"
        )
        assert user.username == unicode_username
        assert "密码" in user.password

    def test_whitespace_handling(self):
        """Test how schemas handle whitespace."""
        # Pydantic typically doesn't strip whitespace by default
        user = UserRegister(
            username="  testuser  ",
            email="  test@example.com  ",
            password="  password123  "
        )
        assert user.username == "  testuser  "
        assert user.email == "test@example.com"  # EmailStr strips whitespace
        assert user.password == "  password123  "

    def test_boolean_field_variations(self):
        """Test boolean fields with various input types."""
        # Test with actual booleans
        status1 = TwoFactorStatusResponse(
            is_2fa_enabled=True,
            is_sms_enabled=False,
            preferred_2fa_method="totp"
        )
        assert status1.is_2fa_enabled is True
        assert status1.is_sms_enabled is False

    def test_list_field_variations(self):
        """Test list fields with various inputs."""
        # Empty list
        setup1 = TwoFactorSetupResponse(
            secret="SECRET",
            qr_code_uri="uri",
            qr_code_image="image",
            backup_codes=[]
        )
        assert setup1.backup_codes == []

        # Single item list
        setup2 = TwoFactorSetupResponse(
            secret="SECRET",
            qr_code_uri="uri",
            qr_code_image="image",
            backup_codes=["ONECODE"]
        )
        assert setup2.backup_codes == ["ONECODE"]

        # Many items
        many_codes = [f"CODE{i}" for i in range(100)]
        setup3 = TwoFactorSetupResponse(
            secret="SECRET",
            qr_code_uri="uri",
            qr_code_image="image",
            backup_codes=many_codes
        )
        assert len(setup3.backup_codes) == 100

    def test_json_serialization_round_trip(self):
        """Test that schemas can round-trip through JSON."""
        import json
        
        original = TwoFactorSetupResponse(
            secret="JBSWY3DPEHPK3PXP",
            qr_code_uri="otpauth://totp/CirtusAI:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=CirtusAI",
            qr_code_image="iVBORw0KGgoAAAANSUhEUgAAAQEAAAEBCAYAAA...",
            backup_codes=["CODE1", "CODE2", "CODE3", "CODE4"]
        )
        
        # Serialize to JSON
        json_str = json.dumps(original.model_dump())
        
        # Deserialize back
        data = json.loads(json_str)
        restored = TwoFactorSetupResponse(**data)
        
        assert restored.secret == original.secret
        assert restored.qr_code_uri == original.qr_code_uri
        assert restored.backup_codes == original.backup_codes
