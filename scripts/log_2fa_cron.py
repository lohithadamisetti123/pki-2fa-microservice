#!/usr/bin/env python3
import datetime
import sys

from app.crypto_utils import read_seed_from_file, generate_totp_code

def main():
    try:
        hex_seed = read_seed_from_file()
    except FileNotFoundError:
        print("Seed not decrypted yet", file=sys.stderr)
        return

    try:
        code = generate_totp_code(hex_seed)
    except Exception as e:
        print(f"Error generating TOTP: {e}", file=sys.stderr)
        return

    # UTC timestamp
    now = datetime.datetime.now(datetime.timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - 2FA Code: {code}")

if __name__ == "__main__":
    main()
