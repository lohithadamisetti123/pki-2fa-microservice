import base64
import subprocess

from app.crypto_utils import (
    load_private_key,
    load_public_key,
    sign_message,
    encrypt_with_public_key,
)

def main():
    commit_hash = subprocess.check_output(
        ["git", "log", "-1", "--format=%H"],
        encoding="utf-8",
    ).strip()

    student_private = load_private_key("student_private.pem")
    instructor_public = load_public_key("instructor_public.pem")

    signature = sign_message(commit_hash, student_private)
    encrypted_sig = encrypt_with_public_key(signature, instructor_public)
    encrypted_sig_b64 = base64.b64encode(encrypted_sig).decode("utf-8")

    print("Commit Hash:")
    print(commit_hash)
    print("\nEncrypted Signature (base64, single line):")
    print(encrypted_sig_b64)

if __name__ == "__main__":
    main()
