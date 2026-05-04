import base64
import os
from cryptography.fernet import Fernet
import datetime

def _mask_string(value, visible_chars=4):    
    """Mask a string showing only the last N characters."""
    if not value or len(value) <= visible_chars:
        return "*" * len(value)
    return "*" * (len(value) - visible_chars) + value[-visible_chars:]

def decrypt(encryptedValue):
    salt = os.getenv("DECRYPT_SALT", "default_salt")
    decrypted_bytes = base64.b64decode(encryptedValue.encode())
    cipher = Fernet(base64.urlsafe_b64encode(salt.encode().ljust(32)[:32]))
    return cipher.decrypt(decrypted_bytes).decode()


def encrypt(plainValue):
    salt = os.getenv("DECRYPT_SALT", "default_salt")
    cipher = Fernet(base64.urlsafe_b64encode(salt.encode().ljust(32)[:32]))
    encrypted_bytes = cipher.encrypt(plainValue.encode())
    return base64.b64encode(encrypted_bytes).decode()

def _unix_to_iso_compact_tz(ts: int, tz_offset_hours: int = 0) -> str:
    tz = datetime.timezone(datetime.timedelta(hours=tz_offset_hours))
    return datetime.datetime.fromtimestamp(ts, tz).strftime('%Y%m%dT%H%M%S')