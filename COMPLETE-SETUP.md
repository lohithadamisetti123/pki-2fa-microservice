# Complete PKI-2FA Microservice Setup

Follow these steps to complete the task:

## 1. Clone Repository
```bash
git clone https://github.com/lohithadamisetti123/pki-2fa-microservice
cd pki-2fa-microservice
```

## 2. Generate RSA Keys
Create `generate_keys.py`:
```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)

public_key = private_key.public_key()

with open('student_private.pem', 'wb') as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open('student_public.pem', 'wb') as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print('Keys generated successfully')
```

Run: `python generate_keys.py`

## 3. Download instructor_public.pem
```bash
curl -o instructor_public.pem https://partnr-public.s3.us-east-1.amazonaws.com/gpp-resources/instructor_public.pem
```

## 4. Request Encrypted Seed
Create `request_seed.py` and run it

## 5. Create Remaining Files
See next steps
