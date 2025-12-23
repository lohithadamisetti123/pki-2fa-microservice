#!/usr/bin/env python3
import subprocess
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Get commit hash
result = subprocess.run(
    ["git", "log", "-1", "--format=%H"],
    capture_output=True,
    text=True
)
commit_hash = result.stdout.strip()

# Load student private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Sign commit hash
message = commit_hash.encode("utf-8")
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Load instructor public key
with open("instructor_public.pem", "rb") as f:
    instructor_key = serialization.load_pem_public_key(f.read())

# Encrypt signature
encrypted_signature = instructor_key.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Base64 encode
proof = base64.b64encode(encrypted_signature).decode("utf-8")

# Output
print(f"COMMIT HASH: {commit_hash}")
print(f"\nENCRYPTED SIGNATURE:\n{proof}")
