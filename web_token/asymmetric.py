
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes, serialization


private_key = open("rsa.key.pub").read()
private_key = serialization.load_ssh_private_key(private_key.encode(), password=b'')

pub_key = open("rsa.key.pub").read()
key = serialization.load_ssh_public_key(pub_key.encode())

0/0
# Create a message to sign
message = b'This is the message to sign'

# Sign the message with the private key
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Verify the signature with the public key
try:
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Signature is valid")
except InvalidSignature:
    print("Signature is invalid")
