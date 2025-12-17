import requests
import json

student_id = "23MH1A4413"  # Replace with your student ID
github_repo_url = "https://github.com/lohithadamisetti123/pki-2fa-microservice"

with open('student_public.pem', 'r') as f:
    public_key = f.read()

payload = {
    "student_id": student_id,
    "github_repo_url": github_repo_url,
    "public_key": public_key
}

response = requests.post(
    "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/",
    json=payload,
    timeout=10
)

data = response.json()
if data.get('status') == 'success':
    with open('encrypted_seed.txt', 'w') as f:
        f.write(data['encrypted_seed'])
    print("✓ Encrypted seed saved to encrypted_seed.txt")
else:
    print("✗ Error:", data)
