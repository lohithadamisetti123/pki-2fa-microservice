#!/usr/bin/env python3
import os
import pyotp
import base64
from datetime import datetime

def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode('utf-8').rstrip('=')

try:
    seed_file = '/data/seed.txt'
    if not os.path.exists(seed_file):
        print('Seed file not found', file=__import__('sys').stderr)
        exit(1)
    
    with open(seed_file, 'r') as f:
        hex_seed = f.read().strip()
    
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    code = totp.now()
    
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - 2FA Code: {code}')
    
except Exception as e:
    print(f'Error: {str(e)}', file=__import__('sys').stderr)
    exit(1)
