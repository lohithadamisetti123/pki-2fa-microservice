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
