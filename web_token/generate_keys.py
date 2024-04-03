"""
Generate a private/public key pair
"""
from cryptography.hazmat.primitives.asymmetric import rsa


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

print(private_key.private_bytes(encoding="base64"))
print()
print(public_key)
