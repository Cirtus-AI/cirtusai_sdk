from cirtusai import CirtusAIClient
client = CirtusAIClient("http://localhost:8000")

# Register with automatic 2FA setup
setup_response = client.auth.register(
    username="tanya",
    email="wangweijia621@gmail.com",
    password="123",
    preferred_2fa_method="totp"  # or "sms"
)

print(f"QR Code URL: {setup_response.qr_code_url}")
print(f"Secret Key: {setup_response.secret_key}")
print(f"Backup Codes: {setup_response.backup_codes}")