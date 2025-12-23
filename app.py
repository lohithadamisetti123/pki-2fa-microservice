#!/usr/bin/env python3
import os
import base64
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import pyotp

app = FastAPI()

PRIVATE_KEY_PATH = "/app/student_private.pem"
SEED_FILE_PATH = "/data/seed.txt"

def load_private_key():
    """Load student private key from PEM file"""
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )

def hex_to_base32(hex_seed: str) -> str:
    """Convert 64-char hex seed to base32 encoding"""
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode("utf-8")

def generate_totp_code(hex_seed: str) -> str:
    """Generate current TOTP code from hex seed"""
    try:
        b32_seed = hex_to_base32(hex_seed)
        totp = pyotp.TOTP(b32_seed, digits=6, interval=30, digest=hashlib.sha1)
        return totp.now()
    except Exception as e:
        raise ValueError(f"Failed to generate TOTP: {str(e)}")

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """Verify TOTP code with ±1 period tolerance"""
    try:
        b32_seed = hex_to_base32(hex_seed)
        totp = pyotp.TOTP(b32_seed, digits=6, interval=30, digest=hashlib.sha1)
        return totp.verify(code, valid_window=valid_window)
    except Exception:
        return False

class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class Verify2FARequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
async def decrypt_seed(request: DecryptSeedRequest):
    """Decrypt encrypted seed and store at /data/seed.txt"""
    try:
        # Load private key
        private_key = load_private_key()
        
        # Base64 decode the encrypted seed
        encrypted_bytes = base64.b64decode(request.encrypted_seed)
        
        # Decrypt using RSA/OAEP with SHA-256
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decode to UTF-8 string
        hex_seed = decrypted_bytes.decode("utf-8").strip()
        
        # Validate: must be 64-character hex string
        if len(hex_seed) != 64:
            raise ValueError(f"Invalid seed length: {len(hex_seed)}, expected 64")
        
        if not all(c in '0123456789abcdef' for c in hex_seed.lower()):
            raise ValueError("Seed contains invalid hex characters")
        
        # Create /data directory if it doesn't exist
        Path("/data").mkdir(parents=True, exist_ok=True)
        
        # Write seed to file
        with open(SEED_FILE_PATH, "w") as f:
            f.write(hex_seed)
        
        # Set proper permissions
        os.chmod(SEED_FILE_PATH, 0o644)
        
        return {"status": "ok"}
    
    except Exception as e:
        print(f"Decryption error: {str(e)}")
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
async def generate_2fa():
    """Generate current TOTP code"""
    try:
        # Check if seed file exists
        if not os.path.exists(SEED_FILE_PATH):
            raise HTTPException(
                status_code=500, 
                detail="Seed not decrypted yet"
            )
        
        # Read hex seed from file
        with open(SEED_FILE_PATH, "r") as f:
            hex_seed = f.read().strip()
        
        # Generate TOTP code
        code = generate_totp_code(hex_seed)
        
        # Calculate remaining validity seconds (0-29)
        now = int(time.time())
        valid_for = 30 - (now % 30)
        
        return {
            "code": code,
            "valid_for": valid_for
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Generate 2FA error: {str(e)}")
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

@app.post("/verify-2fa")
async def verify_2fa(request: Verify2FARequest):
    """Verify TOTP code with ±1 period tolerance"""
    try:
        # Validate code is provided
        if not hasattr(request, 'code') or not request.code:
            raise HTTPException(status_code=400, detail="Missing code")
        
        # Check if seed file exists
        if not os.path.exists(SEED_FILE_PATH):
            raise HTTPException(
                status_code=500,
                detail="Seed not decrypted yet"
            )
        
        # Read hex seed from file
        with open(SEED_FILE_PATH, "r") as f:
            hex_seed = f.read().strip()
        
        # Verify TOTP code with ±1 period tolerance
        is_valid = verify_totp_code(hex_seed, request.code, valid_window=1)
        
        return {"valid": is_valid}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Verify 2FA error: {str(e)}")
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
