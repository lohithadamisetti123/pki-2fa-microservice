# PKI-Based 2FA Microservice

A secure, containerized microservice demonstrating enterprise-grade security practices through Public Key Infrastructure (PKI) and Time-based One-Time Password (TOTP) two-factor authentication.

## Features

- RSA 4096-bit encryption for secure seed transmission
- TOTP-based 2FA for user verification
- REST API endpoints for seed decryption, 2FA code generation, and code verification
- Docker containerization with persistent storage
- Cron job scheduling for automatic TOTP logging
- Multi-stage Docker builds for optimized image size

## Setup

1. Clone the repository
2. Generate RSA key pair
3. Download instructor public key
4. Request encrypted seed from API
5. Build and run Docker container
6. Test endpoints

## API Endpoints

- `POST /decrypt-seed` - Decrypt encrypted seed
- `GET /generate-2fa` - Generate current TOTP code
- `POST /verify-2fa` - Verify TOTP code


COMMIT HASH: 9539be6622056dd0ea22b5bfa484ff3477504f49

ENCRYPTED SIGNATURE:
XL2cJFGFvYgtkr2dCtEGqtdpezII91T/IjvNFjZeMKeCh/6y9DyrcT5lWwcJHVowMfG91nJ4gq2OuQ9GMvlBFtjfV/Jxj6u/oMo3Eze+szidioGbqDWGIBSDA5luaRU+gRHRn2dYA2/368cjN/0IVT5/YncMyuQkxTK+zgT6D4rHFKAhXP9ryWZrp1j68mac+H8O92iK1iFlGz1fIeivtEjDtpbNYxN56ZVL79ane9QzG+/pHKSOGVyTl9ZetxBfO3f6DXBEKtYUAjF1WfWkuUcxFnFoeqsNkPp/v5avcTcDqIfaZ/MdNwm2irZhXmKippJcmjDZuCMv3TTqS7/C2/gP69yK5BNymmmP2wwE28x9ZR++m4FbC0rCtLM5Dhuc9VDmI+VnwGQppQMwj6KN2Y5m8fQbUDGK/B6m2id+6NV/9OlpR2M4q0SpE6X/N2OpeElWOcbJSEnntKL4lAlu/HZw1kG48gxKBDiNhpH4+F5HqXSxYs2h6lSZ0qce25asT4pQuxoHiEmzkyK9O8UKs9Yi81LWmRzYkXGtzMvB1ju/BnuaLN7yZ+cIWzs6Wgeq+hn46/26wKSHyDWDh1QD8Tr5uMHQAPgryOH/LjpahmoyHEzOKXWHkuawzXrol1+W7R9SUY5ck2xbKqNIkKdKd80p4O4/XfST2PV4ALtCFDh+VmxTZWkSA3HVN2+mei+7l03LCo52Tt6szTZqU3Nbh21k/igRXkkQlG/29hNZslQcg3dU0g2/PnK4TCIYne6l4n3zb3F+uHN9IwSPr4lasqseYH4asDzmbbgXvzNF6vKEs724+HLbFwhS3ADuo1b+lzzAyNH1Lz8lf6amOnkdw3kXlf7Sgr3Cf6BDYk1uBblTmMVZNqGKm5wcTHx4Cicv7zW+5nVQIcaAUk3V7ugT/H/hqNdQpaYTbctEECHIdwZq4OdWeA4+TYMc47YPzc+1GOzYH/QvEP5apQAJ1EV5tYnHiv7iUsqrKtwpVJtN3y91Syzeznmo1KadP6ewo6k0dFIOhMSH9Rvwi7daiikCyWVMUMUmh13T/cl8p5QbOWE2fqDy4awqEnIhWyH0skuVfJHz23VoP3eQ8EIbmbgLeOJcl9silbQ2sTo59QuOkqYP+01np64J3MyyFv7WoIpjk49wZ3LF4dq/9yflYchRVh3HWQVl1WymG1wWFm2fVXkGZwpDvduV6T23TX6kPIEPr0NyHLdstCFWgyusuG/CzmHF4F3A7oO9kBYmHH59d1JekQc9R8scGM43T+e+vfKwrOtz2tVkyiyWIPhizQC5wmPZtFrM0xtwA2sNKUC7B62OI/QXR/NZqVIIWFFx8a3hr+PyROAr/pAYasu+Ufrtxg==
