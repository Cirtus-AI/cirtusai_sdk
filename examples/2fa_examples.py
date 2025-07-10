#!/usr/bin/env python3
"""
CirtusAI SDK Examples with Two-Factor Authentication

This file demonstrates how to use the CirtusAI Python SDK with comprehensive 2FA support.
Run different examples by calling the specific functions.

Examples included:
1. User registration with automatic 2FA setup
2. Two-step login flow
3. One-step login flow (convenience method)
4. 2FA management (status, disable, debug)
5. Error handling
6. Async client usage

Requirements:
- CirtusAI backend running on http://localhost:8000
- Authenticator app (Google Authenticator, Authy, etc.)
"""

import asyncio
import base64
import io
from PIL import Image
from cirtusai import CirtusAIClient
from cirtusai.async_ import AsyncCirtusAIClient
from cirtusai.auth import TwoFactorAuthenticationError


def example_registration_and_2fa_setup():
    """Example 1: Register new user with automatic 2FA setup"""
    print("=== Example 1: User Registration with 2FA Setup ===")
    
    client = CirtusAIClient(base_url="http://localhost:8000")
    
    try:
        # Register new user - 2FA is automatically set up
        setup_info = client.auth.register(
            username="example_user",
            email="example@test.com",
            password="SecurePass123!",
            preferred_2fa_method="totp"
        )
        
        print("✅ User registered successfully!")
        print(f"📱 TOTP Secret: {setup_info.secret}")
        print(f"🔗 QR URI: {setup_info.qr_code_uri}")
        print(f"🔢 Backup Codes: {setup_info.backup_codes}")
        
        # Save QR code as image file
        qr_image_data = base64.b64decode(setup_info.qr_code_image)
        with open("qr_code.png", "wb") as f:
            f.write(qr_image_data)
        print("💾 QR code saved as qr_code.png")
        
        # Display QR code if PIL is available
        try:
            img = Image.open(io.BytesIO(qr_image_data))
            img.show()
            print("📱 QR code displayed - scan with your authenticator app")
        except ImportError:
            print("📱 Install PIL to display QR code: pip install Pillow")
        
        print("\n🎯 Next steps:")
        print("1. Scan the QR code with your authenticator app")
        print("2. Use the TOTP codes for login")
        
    except Exception as e:
        print(f"❌ Registration failed: {e}")
    finally:
        client.close()


def example_two_step_login():
    """Example 2: Two-step login flow (recommended for interactive apps)"""
    print("\n=== Example 2: Two-Step Login Flow ===")
    
    client = CirtusAIClient(base_url="http://localhost:8000")
    
    try:
        # Step 1: Initial login
        print("🔐 Step 1: Initial login...")
        login_result = client.auth.login("example@test.com", "SecurePass123!")
        
        if hasattr(login_result, 'requires_2fa') and login_result.requires_2fa:
            print("🔒 2FA required!")
            print(f"📱 Preferred method: {login_result.preferred_method}")
            print(f"⏰ Temporary token expires in 5 minutes")
            
            # In a real app, you'd get this from user input
            totp_code = input("Enter your 6-digit TOTP code: ")
            
            # Step 2: Verify 2FA
            print("🔐 Step 2: Verifying 2FA...")
            token = client.auth.verify_2fa(login_result.temporary_token, totp_code)
            
            print("✅ 2FA verification successful!")
            print(f"🎫 Access token: {token.access_token[:20]}...")
            
            # Set token for authenticated requests
            client.set_token(token.access_token)
            
        else:
            print("✅ No 2FA required - direct login successful!")
            client.set_token(login_result.access_token)
        
        # Test authenticated request
        status = client.auth.get_2fa_status()
        print(f"📊 2FA Status: {status}")
        
    except TwoFactorAuthenticationError as e:
        print(f"❌ 2FA failed: {e}")
        if "time_step" in str(e):
            print("💡 Tip: Check your device time synchronization")
    except Exception as e:
        print(f"❌ Login failed: {e}")
    finally:
        client.close()


def example_one_step_login():
    """Example 3: One-step login flow (convenience method)"""
    print("\n=== Example 3: One-Step Login Flow ===")
    
    client = CirtusAIClient(base_url="http://localhost:8000")
    
    try:
        # Get TOTP code from user
        totp_code = input("Enter your current 6-digit TOTP code: ")
        
        # Login with 2FA in one step
        token = client.auth.login_with_2fa(
            "example@test.com",
            "SecurePass123!",
            totp_code
        )
        
        print("✅ One-step login successful!")
        print(f"🎫 Access token: {token.access_token[:20]}...")
        
        # Set token and test
        client.set_token(token.access_token)
        status = client.auth.get_2fa_status()
        print(f"📊 2FA Status: {status}")
        
    except TwoFactorAuthenticationError as e:
        print(f"❌ 2FA failed: {e}")
        if "Invalid TOTP code" in str(e):
            print("💡 Tip: Make sure you're using the current code from your authenticator app")
    except Exception as e:
        print(f"❌ Login failed: {e}")
    finally:
        client.close()


def example_2fa_management():
    """Example 4: 2FA management and debugging"""
    print("\n=== Example 4: 2FA Management ===")
    
    client = CirtusAIClient(base_url="http://localhost:8000")
    
    try:
        # Login first
        totp_code = input("Enter your TOTP code to login: ")
        token = client.auth.login_with_2fa("example@test.com", "SecurePass123!", totp_code)
        client.set_token(token.access_token)
        
        # Check 2FA status
        print("📊 Checking 2FA status...")
        status = client.auth.get_2fa_status()
        print(f"✅ 2FA enabled: {status.is_2fa_enabled}")
        print(f"📱 Preferred method: {status.preferred_2fa_method}")
        print(f"📧 SMS enabled: {status.is_sms_enabled}")
        
        # Debug TOTP codes
        print("\n🔍 Debugging TOTP codes...")
        debug_info = client.auth.debug_2fa()
        print(f"🕒 Server time: {debug_info['current_server_time']}")
        print("⏰ Valid codes right now:")
        for step, code in debug_info["valid_codes"].items():
            print(f"   {step}: {code}")
        
        # Get QR code
        print("\n📱 Getting QR code...")
        qr_bytes = client.auth.get_qr_code()
        with open("current_qr.png", "wb") as f:
            f.write(qr_bytes)
        print("💾 Current QR code saved as current_qr.png")
        
        # Option to disable 2FA
        disable = input("\n❓ Disable 2FA? (y/N): ").lower()
        if disable == 'y':
            password = input("Enter your password: ")
            totp_code = input("Enter current TOTP code: ")
            
            result = client.auth.disable_2fa(totp_code, password)
            print(f"✅ 2FA disabled: {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()


def example_error_handling():
    """Example 5: Comprehensive error handling"""
    print("\n=== Example 5: Error Handling ===")
    
    client = CirtusAIClient(base_url="http://localhost:8000")
    
    # Test wrong password
    print("🧪 Testing wrong password...")
    try:
        client.auth.login("example@test.com", "wrong_password")
    except Exception as e:
        print(f"✅ Caught wrong password: {e}")
    
    # Test wrong TOTP code
    print("\n🧪 Testing wrong TOTP code...")
    try:
        login_result = client.auth.login("example@test.com", "SecurePass123!")
        if hasattr(login_result, 'requires_2fa'):
            client.auth.verify_2fa(login_result.temporary_token, "000000")
    except TwoFactorAuthenticationError as e:
        print(f"✅ Caught wrong TOTP: {e}")
        if "Valid codes right now:" in str(e):
            print("💡 Error includes valid codes for debugging!")
    
    # Test expired temporary token
    print("\n🧪 Testing expired token...")
    try:
        client.auth.verify_2fa("expired.token.here", "123456")
    except Exception as e:
        print(f"✅ Caught expired token: {e}")
    
    client.close()


async def example_async_client():
    """Example 6: Async client usage"""
    print("\n=== Example 6: Async Client ===")
    
    client = AsyncCirtusAIClient(base_url="http://localhost:8000")
    
    try:
        # Async registration
        print("🔐 Async registration...")
        setup_info = await client.auth.register(
            username="async_user",
            email="async@test.com",
            password="SecurePass123!",
            preferred_2fa_method="totp"
        )
        print("✅ Async registration successful!")
        print(f"📱 Secret: {setup_info.secret}")
        
        # Async login
        print("\n🔐 Async login...")
        totp_code = input("Enter TOTP code for async user: ")
        token = await client.auth.login_with_2fa(
            "async@test.com",
            "SecurePass123!",
            totp_code
        )
        
        await client.set_token(token.access_token)
        print("✅ Async login successful!")
        
        # Async 2FA status
        status = await client.auth.get_2fa_status()
        print(f"📊 Async 2FA status: {status}")
        
    except Exception as e:
        print(f"❌ Async error: {e}")
    finally:
        await client.close()


def main():
    """Run all examples"""
    print("🚀 CirtusAI SDK Examples with Two-Factor Authentication")
    print("="*60)
    
    examples = [
        ("Registration with 2FA Setup", example_registration_and_2fa_setup),
        ("Two-Step Login Flow", example_two_step_login),
        ("One-Step Login Flow", example_one_step_login),
        ("2FA Management", example_2fa_management),
        ("Error Handling", example_error_handling),
        ("Async Client", lambda: asyncio.run(example_async_client())),
    ]
    
    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    print("0. Run all examples")
    
    try:
        choice = int(input("\nSelect example (0-6): "))
        
        if choice == 0:
            for name, func in examples:
                print(f"\n{'='*20} {name} {'='*20}")
                func()
        elif 1 <= choice <= len(examples):
            examples[choice-1][1]()
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except ValueError:
        print("❌ Please enter a number")


if __name__ == "__main__":
    main()
