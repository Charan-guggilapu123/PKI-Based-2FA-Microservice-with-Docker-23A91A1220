from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

commit_hash = "b42345844f9c91eecfc2f505a6bcb078d3c35217"

with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
    )

signature = private_key.sign(
    commit_hash.encode("utf-8"),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    ),
    hashes.SHA256(),
)

with open("signature.bin", "wb") as f:
    f.write(signature)

print("OK: signature.bin created")
