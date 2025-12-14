import json
import requests
from pathlib import Path

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

STUDENT_ID = "23A91A1220"
GITHUB_REPO_URL = "https://github.com/Charan-guggilapu123/PKI-Based-2FA-Microservice-with-Docker-23A91A1220"
PUBLIC_KEY_PATH = Path("student_public.pem")
OUT_PATH = Path("encrypted_seed.txt")

def main():
    public_key = PUBLIC_KEY_PATH.read_text()

    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": public_key,
    }

    r = requests.post(API_URL, json=payload, timeout=20)
    r.raise_for_status()
    data = r.json()

    if "encrypted_seed" not in data:
        raise RuntimeError(f"Unexpected response: {data}")

    OUT_PATH.write_text(data["encrypted_seed"])
    print("Encrypted seed saved to encrypted_seed.txt")

if __name__ == "__main__":
    main()
