import json
import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"

STUDENT_ID = "23MH1A4413"
GITHUB_REPO_URL = "https://github.com/lohithadamisetti123/pki-2fa-microservice"

def main():
    with open("student_public.pem", "r", encoding="utf-8") as f:
        public_key_pem = f.read()

    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": public_key_pem,
    }

    resp = requests.post(API_URL, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "success":
        raise SystemExit(f"API error: {data}")

    encrypted_seed = data["encrypted_seed"]

    with open("encrypted_seed.txt", "w", encoding="utf-8") as f:
        f.write(encrypted_seed.strip())

    print("Encrypted seed saved to encrypted_seed.txt")

if __name__ == "__main__":
    main()
