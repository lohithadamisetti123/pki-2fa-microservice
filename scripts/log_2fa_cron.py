#!/usr/bin/env python3
"""Cron script to log 2FA codes every minute"""
import sys
import os
from datetime import datetime, timezone
import hashlib
import base64
import pyotp

SEED_PATH = "/data/seed.txt"

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
        print(f"Failed to generate TOTP: {str(e)}", file=sys.stderr)
        return None

def main():
    """Main cron job logic"""
    try:
        # Check if seed file exists
        if not os.path.exists(SEED_PATH):
            print("Seed file not found", file=sys.stderr)
            return
        
        # Read hex seed from file
        with open(SEED_PATH, "r") as f:
            hex_seed = f.read().strip()
        
        # Generate current TOTP code
        code = generate_totp_code(hex_seed)
        if code is None:
            return
        
        # Get current UTC timestamp
        now_utc = datetime.now(timezone.utc)
        ts = now_utc.strftime("%Y-%m-%d %H:%M:%S")
        
        # Print in EXACT format required:
        # YYYY-MM-DD HH:MM:SS - 2FA Code: XXXXXX
        print(f"{ts} - 2FA Code: {code}")
        sys.stdout.flush()
    
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()
