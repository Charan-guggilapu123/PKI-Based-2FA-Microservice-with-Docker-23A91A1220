import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


def load_private_key(path: str):
    with open(path, "rb") as f:
        return load_pem_private_key(f.read(), password=None)


def load_public_key(path: str):
    with open(path, "rb") as f:
        return load_pem_public_key(f.read())


def decrypt_seed(encrypted_b64: str, private_key) -> str:
    ciphertext = base64.b64decode(encrypted_b64)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    seed = plaintext.decode("utf-8").strip()

    if len(seed) != 64 or any(c not in "0123456789abcdef" for c in seed):
        raise ValueError("Invalid seed format")

    return seed


def sign_commit(commit_hash: str, private_key) -> bytes:
    return private_key.sign(
        commit_hash.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )


def encrypt_signature(signature: bytes, public_key) -> bytes:
    return public_key.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

