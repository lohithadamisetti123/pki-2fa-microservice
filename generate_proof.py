#!/usr/bin/env python3
"""
Generate commit proof: sign commit hash with student private key,
then encrypt the signature with instructor public key.
"""

import base64
import sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


def sign_message(message: str, private_key):
    """Sign a message using RSA-PSS with SHA-256"""
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """Encrypt data using RSA/OAEP with SHA-256"""
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def generate_proof(commit_hash: str):
    """Generate commit proof"""
    # Load student private key
    with open('student_private.pem', 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    
    # Sign commit hash
    signature = sign_message(commit_hash, private_key)
    
    # Load instructor public key
    with open('instructor_public.pem', 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    
    # Encrypt signature
    encrypted_signature = encrypt_with_public_key(signature, public_key)
    
    # Base64 encode
    encrypted_signature_b64 = base64.b64encode(encrypted_signature).decode('utf-8')
    
    return encrypted_signature_b64


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 generate_proof.py mmit_hash>")
        sys.exit(1)
    
    commit_hash = sys.argv[1]
    proof = generate_proof(commit_hash)
    print(proof)
