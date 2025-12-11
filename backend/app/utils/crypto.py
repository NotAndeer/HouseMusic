"""Utilities for encrypting and decrypting sensitive data."""

import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.core.config import settings


# Derive a 32-byte key from the secret key using PBKDF2
def _get_fernet_key() -> bytes:
    """Derive a Fernet-compatible key from the app secret."""
    password = settings.app_encryption_key.encode()
    salt = b"housemusic_salt_2025"  # Fixed salt; for higher security, store per-record
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


_fernet = Fernet(_get_fernet_key())


def encrypt_data(data: str) -> str:
    """Encrypt a string and return the base64-encoded ciphertext."""
    if not data:
        return ""
    ciphertext = _fernet.encrypt(data.encode())
    return base64.urlsafe_b64encode(ciphertext).decode()


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt a base64-encoded ciphertext and return the original string."""
    if not encrypted_data:
        return ""
    try:
        ciphertext = base64.urlsafe_b64decode(encrypted_data.encode())
        plaintext = _fernet.decrypt(ciphertext)
        return plaintext.decode()
    except (InvalidToken, ValueError) as e:
        raise ValueError("Decryption failed: invalid or corrupted data") from e