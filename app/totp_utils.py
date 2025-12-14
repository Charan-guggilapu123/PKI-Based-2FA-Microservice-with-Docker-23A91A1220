import base64
import pyotp
import time


def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode("utf-8")


def generate_totp(hex_seed: str) -> tuple[str, int]:
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)

    code = totp.now()
    remaining = totp.interval - (int(time.time()) % totp.interval)

    return code, remaining


def verify_totp(hex_seed: str, code: str) -> bool:
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=1)
