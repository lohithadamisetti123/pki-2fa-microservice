import requests
import json

STUDENT_ID = "23MH1A4413"
GITHUB_URL = "https://github.com/lohithadamisetti123/pki-2fa-microservice"
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"

print("[*] Step 1: Reading student public key...")
with open("student_public.pem", "r") as f:
    public_key_pem = f.read()
print(f"[*] Read {len(public_key_pem)} bytes")

print("[*] Step 2: Preparing request payload...")
payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": GITHUB_URL,
    "public_key": public_key_pem
}
print("[*] Payload ready")

print(f"[*] Step 3: Sending POST to {API_URL}...")
try:
    response = requests.post(API_URL, json=payload, timeout=15)
    print(f"[*] HTTP {response.status_code}")
    
    result = response.json()
    print("[*] JSON parsed")
    
    if "encrypted_seed" in result:
        encrypted_seed = result["encrypted_seed"]
        with open("encrypted_seed.txt", "w") as f:
            f.write(encrypted_seed)
        print("\n[SUCCESS] Encrypted seed saved!")
        print(f"[SUCCESS] File: encrypted_seed.txt")
        print(f"[SUCCESS] Length: {len(encrypted_seed)} characters")
    else:
        print(f"\n[ERROR] Response keys: {list(result.keys())}")
        print(f"[ERROR] Response: {json.dumps(result, indent=2)}")
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
