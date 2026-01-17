import sys, base64
from pathlib import Path
from app.crypto_utils import load_private_key, load_public_key, sign_commit, encrypt_signature

OUT_PATH = Path("encrypted_signature.txt")

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/generate_encrypted_signature.py <commit_hash>")
        sys.exit(1)
    commit_hash = sys.argv[1]

    priv = load_private_key("student_private.pem")
    instr_pub = load_public_key("instructor_public.pem")

    sig = sign_commit(commit_hash, priv)
    enc = encrypt_signature(sig, instr_pub)
    encoded = base64.b64encode(enc).decode("utf-8")
    OUT_PATH.write_text(encoded)
    print(encoded)
    print(f"Encrypted signature written to {OUT_PATH}")

if __name__ == "__main__":
    main()
