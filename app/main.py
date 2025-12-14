from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path

from app.crypto_utils import load_private_key, decrypt_seed
from app.totp_utils import generate_totp, verify_totp

DATA_PATH = Path("/data/seed.txt")
PRIVATE_KEY_PATH = "/app/student_private.pem"

app = FastAPI()
private_key = load_private_key(PRIVATE_KEY_PATH)


class SeedRequest(BaseModel):
    encrypted_seed: str


class CodeRequest(BaseModel):
    code: str


@app.post("/decrypt-seed")
def decrypt_seed_api(req: SeedRequest):
    try:
        seed = decrypt_seed(req.encrypted_seed, private_key)
        DATA_PATH.parent.mkdir(exist_ok=True)
        DATA_PATH.write_text(seed)
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")


@app.get("/generate-2fa")
def generate_2fa():
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    seed = DATA_PATH.read_text().strip()
    code, valid_for = generate_totp(seed)
    return {"code": code, "valid_for": valid_for}


@app.post("/verify-2fa")
def verify_2fa(req: CodeRequest):
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    seed = DATA_PATH.read_text().strip()
    return {"valid": verify_totp(seed, req.code)}
