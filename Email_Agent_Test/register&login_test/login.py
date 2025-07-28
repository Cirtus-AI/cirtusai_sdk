from cirtusai import CirtusAIClient
client = CirtusAIClient("http://localhost:8000")
token = client.auth.login(
    username="tommywang",
    password="123"
)
print(f"Access Token: {token.access_token}")
client.set_token(token.access_token)