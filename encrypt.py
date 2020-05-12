import secrets
from base64 import urlsafe_b64encode, urlsafe_b64decode

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
iterations = 100_000

# TODO: look into all of this


def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=backend,
    )
    return urlsafe_b64encode(kdf.derive(password))


def password_encrypt(
    message: str, password: str, iterations: int = iterations
) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return urlsafe_b64encode(
        b"%b%b%b"
        % (
            salt,
            iterations.to_bytes(4, "big"),
            urlsafe_b64decode(Fernet(key).encrypt(message)),
        )
    )


def password_decrypt(token: bytes, password: str) -> str:
    decoded = urlsafe_b64decode(token)
    salt, iter, token = decoded[:16], decoded[16:20], urlsafe_b64encode(decoded[20:])
    iterations = int.from_bytes(iter, "big")
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token).decode("ascii")
