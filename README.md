# PKI-Based 2FA Microservice 

A secure, containerized authentication microservice implementing PKI (RSA-4096) and TOTP-based two-factor authentication, built with Python, FastAPI, Docker, and cron.

This project demonstrates enterprise-grade security practices including asymmetric cryptography, time-based OTP generation, persistent storage, and automated background jobs in a containerized environment.

## Features

- RSA 4096-bit key pair for secure seed exchange

- RSA/OAEP (SHA-256) decryption of encrypted seed

- RSA-PSS (SHA-256) commit signature for proof of work

- TOTP generation (SHA-1, 30-second window, 6 digits)

- TOTP verification with ±1 time-step tolerance

- Persistent storage using Docker volumes

- Cron job logging 2FA codes every minute (UTC)

- Multi-stage Docker build for optimized image size

## Technology Stack

### anguage: Python 3.11

### Framework: FastAPI

### Cryptography: cryptography

### TOTP: pyotp

### Containerization: Docker, Docker Compose

### Background Jobs: cron (inside container)

## Project Structure
bash 
PKI-Based-2FA-Microservice/
├── app/
│   ├── main.py              # FastAPI application
│   ├── crypto_utils.py      # RSA decryption & signing logic
│   └── totp_utils.py        # TOTP generation & verification
├── scripts/
│   ├── generate_keys.py     # RSA key generation
│   ├── request_seed.py      # Instructor API seed request
│   └── log_2fa_cron.py      # Cron script for logging OTPs
├── cron/
│   └── 2fa-cron             # Cron configuration (LF endings)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── student_private.pem
├── student_public.pem
├── instructor_public.pem
├── .gitattributes
├── .gitignore
└── README.md

## API Endpoints
### Decrypt Seed

POST /decrypt-seed

Request

{
  "encrypted_seed": "<base64 string>"
}


Response


{ "status": "ok" }


Stores decrypted seed at /data/seed.txt.

2. Generate 2FA Code

    GET /generate-2fa
    
    Response

{
  "code": "123456",
  "valid_for": 17
}

3. Verify 2FA Code

   POST /verify-2fa

    Request

{
  "code": "123456"
}

 Response
 
{
  "valid": true
}

Supports ±1 period tolerance (±30 seconds).

# TOTP Configuration

- Algorithm: SHA-1

- Period: 30 seconds

- Digits: 6

- Seed: 64-char hex → Base32 (required)

## Cron Job

- Runs every minute

- Reads seed from /data/seed.txt

- Generates current TOTP

- Logs to /cron/last_code.txt

### Log format
bash
YYYY-MM-DD HH:MM:SS - 2FA Code: XXXXXX

All timestamps use UTC.

## Docker & Persistence

- Multi-stage Docker build

## Volumes:

/data → decrypted seed

/cron → cron output logs

- API exposed on port 8080

- Cron daemon and FastAPI start together

How to Run Locally
bash
docker compose build
docker compose up -d

Testing
# Decrypt seed

curl -X POST http://localhost:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d '{"encrypted_seed":"<base64>"}'

# Generate OTP

curl http://localhost:8080/generate-2fa

# Verify OTP

curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d '{"code":"123456"}'

# Cron verification:

- docker exec pki-2fa cat /cron/last_code.txt

- Security Notes

- RSA keys committed only for assignment purposes

- Keys must never be reused in production

- Seed is never exposed via API after decryption

- All cryptographic parameters strictly match specification

## Assignment Compliance

- RSA-4096 with OAEP-SHA256 ✔

- RSA-PSS commit signature ✔

- TOTP (SHA-1, 30s, 6 digits) ✔

- Persistent storage ✔

- Cron automation ✔

- Docker multi-stage build ✔

- UTC timezone enforced ✔

## Author

Guggilapu Guru Charan

Student ID: 23A91A1220