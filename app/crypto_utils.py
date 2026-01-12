import base64
import os
from typing import Tuple

import pyotp
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric import utils as asym_utils

SEED_PATH = "/data/seed.txt"

def load_private_key(path: str = "student_private.pem") -> rsa.RSAPrivateKey:
    with open(path, "rb") as f:
        key = serialization.load_pem_private_key(f.read(), password=None)
    return key

def load_public_key(path: str) -> rsa.RSAPublicKey:
    with open(path, "rb") as f:
        key = serialization.load_pem_public_key(f.read())
    return key

def decrypt_seed(encrypted_seed_b64: str, private_key: rsa.RSAPrivateKey) -> str:
    ciphertext = base64.b64decode(encrypted_seed_b64)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    hex_seed = plaintext.decode("utf-8").strip()

    if len(hex_seed) != 64:
        raise ValueError("Seed must be 64 hex chars")
    if any(c not in "0123456789abcdef" for c in hex_seed):
        raise ValueError("Seed is not lowercase hex")

    os.makedirs(os.path.dirname(SEED_PATH), exist_ok=True)
    with open(SEED_PATH, "w", encoding="utf-8") as f:
        f.write(hex_seed)

    return hex_seed

def read_seed_from_file() -> str:
    if not os.path.exists(SEED_PATH):
        raise FileNotFoundError("Seed not decrypted yet")
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()

def _hex_seed_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    b32 = base64.b32encode(seed_bytes).decode("utf-8")
    return b32

def generate_totp_code(hex_seed: str) -> str:
    base32_seed = _hex_seed_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)  # SHA‑1, 30s, 6 digits by default
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    base32_seed = _hex_seed_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=valid_window)

def sign_message(message: str, private_key: rsa.RSAPrivateKey) -> bytes:
    msg_bytes = message.encode("utf-8")
    signature = private_key.sign(
        msg_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature

def encrypt_with_public_key(data: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext
