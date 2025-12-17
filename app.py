from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pyotp
import base64
import time
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

app = FastAPI()

# Load private key
with open('student_private.pem', 'rb') as f:
    private_key = serialization.load_pem_private_key(
        f.read(), password=None, backend=default_backend()
    )

SEED_FILE = '/data/seed.txt'

class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class Verify2FARequest(BaseModel):
    code: str

def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode('utf-8').rstrip('=')

def get_remaining_seconds() -> int:
    return 30 - (int(time.time()) % 30)

@app.post("/decrypt-seed")
async def decrypt_seed(request: DecryptSeedRequest):
    try:
        ciphertext = base64.b64decode(request.encrypted_seed)
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        seed_hex = plaintext.decode('utf-8').strip()
        if len(seed_hex) != 64 or not all(c in '0123456789abcdef' for c in seed_hex.lower()):
            raise ValueError('Invalid seed format')
        os.makedirs(os.path.dirname(SEED_FILE), exist_ok=True)
        with open(SEED_FILE, 'w') as f:
            f.write(seed_hex)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
async def generate_2fa():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    with open(SEED_FILE, 'r') as f:
        hex_seed = f.read().strip()
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    code = totp.now()
    valid_for = get_remaining_seconds()
    return {"code": code, "valid_for": valid_for}

@app.post("/verify-2fa")
async def verify_2fa(request: Verify2FARequest):
    if not request.code:
        raise HTTPException(status_code=400, detail="Missing code")
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    with open(SEED_FILE, 'r') as f:
        hex_seed = f.read().strip()
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    valid = totp.verify(request.code, valid_window=1)
    return {"valid": valid}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
