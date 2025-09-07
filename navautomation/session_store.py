# navautomation/session_store.py
from pathlib import Path
import json
from .utils import encrypt_bytes, decrypt_bytes, safe_write_bytes
from typing import Optional, Dict, Any
import os

# session file lives in same folder as this file
_DEFAULT_SESSION = Path(__file__).parent.joinpath("session.nava").resolve()

def _path(p: Optional[str]) -> str:
    if p:
        return p
    return str(_DEFAULT_SESSION)

def save_session(cookies: Dict[str,str], passphrase: str, path: Optional[str]=None) -> None:
    data = {"cookies": cookies, "saved_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime())}
    plain = json.dumps(data, ensure_ascii=False).encode("utf-8")
    enc = encrypt_bytes(plain, passphrase)
    safe_write_bytes(_path(path), enc)

def load_session(passphrase: str, path: Optional[str]=None) -> Dict[str,Any]:
    p = _path(path)
    if not Path(p).exists():
        raise FileNotFoundError("no session")
    blob = Path(p).read_bytes()
    plain = decrypt_bytes(blob, passphrase)
    return json.loads(plain.decode("utf-8"))

def remove_session(path: Optional[str]=None) -> None:
    p = _path(path)
    try:
        Path(p).unlink()
    except Exception:
        pass
