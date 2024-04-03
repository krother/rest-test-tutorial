# ssh-keygen -t rsa
# pip install pyjwt[crypto]


import jwt
payload = {"hello": "world", "anwer": 42}
secret = "r2d2"
token = jwt.encode(payload=payload, key=secret)
token
type(token)
# go to jwt.io and paste the token

private_key = open('rsa.key', 'r').read()
private_key
key = serialization.load_ssh_private_key(private_key.encode(), password=b'')
key
token = jwt.encode(payload=payload, key=key)
token = jwt.encode(payload=payload, key=key, algorithm='RS256')
token
!cat rsa.pub
ls
!cat rsa.key.pub
key
priv
private_key
print(private_key)
token
jwt.get_unverified_header(token)
pub_key = open("rsa.key.pub").read()
pub_key
private_key
key = serialization.load_ssh_public_key(pub_key.encode())
key
jwt.decode(jwt=token, key=key, algorithms=['RS256', ])

