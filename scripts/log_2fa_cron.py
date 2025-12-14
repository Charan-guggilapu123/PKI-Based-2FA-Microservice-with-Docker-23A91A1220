from datetime import datetime, timezone
from pathlib import Path
from app.totp_utils import generate_totp

SEED_FILE = Path("/data/seed.txt")

if not SEED_FILE.exists():
    print("Seed missing")
    exit(1)

seed = SEED_FILE.read_text().strip()
code, _ = generate_totp(seed)

ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
print(f"{ts} - 2FA Code: {code}")
