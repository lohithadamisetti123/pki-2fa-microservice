import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .crypto_utils import (
    decrypt_seed,
    read_seed_from_file,
    generate_totp_code,
    verify_totp_code,
    load_private_key,
)

app = FastAPI()

class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str | None = None

@app.post("/decrypt-seed")
def decrypt_seed_endpoint(payload: DecryptSeedRequest):
    try:
        private_key = load_private_key("student_private.pem")
        decrypt_seed(payload.encrypted_seed, private_key)
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
def generate_2fa():
    try:
        hex_seed = read_seed_from_file()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    code = generate_totp_code(hex_seed)

    period = 30
    now = int(time.time())
    remaining = period - (now % period)

    return {"code": code, "valid_for": remaining}

@app.post("/verify-2fa")
def verify_2fa(payload: VerifyRequest):
    if not payload.code:
        raise HTTPException(status_code=400, detail="Missing code")

    try:
        hex_seed = read_seed_from_file()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    is_valid = verify_totp_code(hex_seed, payload.code, valid_window=1)
    return {"valid": is_valid}
