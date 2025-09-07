# navautomation/utils.py
# توابع کمکی کوچک و ساده
import os, json, base64, time
from pathlib import Path
from typing import Dict, Any, Optional

# cryptography for encrypting session.nava
try:
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.fernet import Fernet
except Exception:
    PBKDF2HMAC = None
    Fernet = None

def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def ensure_crypto():
    if PBKDF2HMAC is None or Fernet is None:
        raise RuntimeError("Install cryptography (pip install cryptography)")

def _derive(passphrase: str, salt: bytes) -> bytes:
    ensure_crypto()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000, backend=default_backend())
    key = kdf.derive(passphrase.encode("utf-8"))
    return base64.urlsafe_b64encode(key)

def encrypt_bytes(plain: bytes, passphrase: str) -> bytes:
    ensure_crypto()
    salt = os.urandom(16)
    key = _derive(passphrase, salt)
    token = Fernet(key).encrypt(plain)
    out = {"v":1, "salt": base64.b64encode(salt).decode("ascii"), "token": base64.b64encode(token).decode("ascii")}
    return json.dumps(out, ensure_ascii=False).encode("utf-8")

def decrypt_bytes(blob: bytes, passphrase: str) -> bytes:
    ensure_crypto()
    j = json.loads(blob.decode("utf-8"))
    if j.get("v") != 1:
        raise ValueError("unsupported_version")
    salt = base64.b64decode(j["salt"])
    token = base64.b64decode(j["token"])
    key = _derive(passphrase, salt)
    return Fernet(key).decrypt(token)

def safe_write_bytes(path: str, data: bytes):
    tmp = path + ".tmp"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        try:
            os.fsync(f.fileno())
        except Exception:
            pass
    os.replace(tmp, path)
