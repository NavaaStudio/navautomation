# navautomation/client.py
from typing import Dict, Any, Optional
from pathlib import Path
import requests

from . import config
from .errors import NavaErr, make_err_from_resp
from .session_store import save_session, load_session, remove_session


class SyncClient:
    """
    کلاینت همگام (requests). فانکشن‌ها کوتاه نام دارن:
      - otp_send(email)
      - otp_ver(email, code)
      - otp_login(email, code)
      - auth_login(user, pass)
      - auth_signup(user, email, pass)
      - msg_send(tt, id, body)
      - msg_fetch(tt, id)
      - msg_edit(mid, body)
      - msg_del(mid)
      - upload(path)
      - join_group(gid)
      - create_group(name, privacy)
      - create_channel(name, broadcast)
      - report(type, target_id, reason)
      - sess_save(passphrase)
      - sess_load(passphrase)
      - sess_rm()
      - whoami()
    """

    def __init__(
        self,
        base: Optional[str] = None,
        api_path: Optional[str] = None,
        session_file: Optional[str] = None,
        timeout: int = 12,
    ):
        self.base = (base or config.DEFAULT_BASE).rstrip("/")
        # مسیر actions.php به عنوان پیش‌فرض
        self.api = api_path or "/src/actions.php"
        if not self.api.startswith("/"):
            self.api = "/" + self.api
        self.url = self.base + self.api

        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "NavaSync/0.2"})
        self.timeout = timeout
        self._session_file = session_file

    # internal helper
    def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            r = self.s.post(self.url, json=payload, timeout=self.timeout)
        except Exception as e:
            raise NavaErr("net_error", details=str(e))

        try:
            data = r.json()
        except Exception:
            if r.ok:
                return {"success": True, "raw_text": r.text}
            raise NavaErr("bad_response", details=r.text[:200])

        if isinstance(data, dict) and data.get("success") is False:
            raise make_err_from_resp(data)
        return data

    # ---- auth / otp ----
    def otp_send(self, email: str) -> Dict[str, Any]:
        return self._post({"action": "send_otp", "email": email})

    def otp_ver(self, email: str, code: str) -> Dict[str, Any]:
        return self._post({"action": "verify_otp", "email": email, "code": code})

    def otp_login(self, email: str, code: str) -> Dict[str, Any]:
        return self._post({"action": "login_by_otp", "email": email, "code": code})

    def auth_login(self, user: str, pwd: str) -> Dict[str, Any]:
        return self._post({"action": "login", "username": user, "password": pwd})

    def auth_signup(self, user: str, email: str, pwd: str) -> Dict[str, Any]:
        return self._post({"action": "signup", "username": user, "email": email, "password": pwd})

    # ---- messages ----
    def msg_send(self, tt: str, id: int, body: str) -> Dict[str, Any]:
        return self._post({"action": "send_message", "target_type": tt, "target_id": int(id), "body": body})

    def msg_fetch(self, tt: str, id: int) -> Dict[str, Any]:
        return self._post({"action": "fetch_messages", "target_type": tt, "target_id": int(id)})

    def msg_edit(self, mid: int, body: str) -> Dict[str, Any]:
        return self._post({"action": "edit_message", "message_id": int(mid), "body": body})

    def msg_del(self, mid: int) -> Dict[str, Any]:
        return self._post({"action": "delete_message", "message_id": int(mid)})

    def react(self, mid: int, emoji: str, remove: bool = False) -> Dict[str, Any]:
        return self._post({"action": "react_message", "message_id": int(mid), "emoji": emoji, "remove": bool(remove)})

    def mark_read(self, from_user: int) -> Dict[str, Any]:
        return self._post({"action": "mark_read", "from_user": int(from_user)})

    # ---- file upload ----
    def upload(self, filepath: str) -> Dict[str, Any]:
        filepath = str(filepath)
        with open(filepath, "rb") as fh:
            files = {"file": (Path(filepath).name, fh)}
            try:
                r = self.s.post(self.base + "/src/storage.php", data={"action": "upload"}, files=files, timeout=self.timeout)
            except Exception as e:
                raise NavaErr("upload_err", details=str(e))
            try:
                data = r.json()
            except Exception:
                if r.ok:
                    return {"success": True, "raw_text": r.text}
                raise NavaErr("upload_bad_response", details=r.text[:200])
            if isinstance(data, dict) and data.get("success") is False:
                raise make_err_from_resp(data)
            return data

    # ---- groups & channels ----
    def join_group(self, gid: int) -> Dict[str, Any]:
        return self._post({"action": "join_group", "group_id": int(gid)})

    def create_group(self, name: str, privacy: str = "public") -> Dict[str, Any]:
        return self._post({"action": "create_group", "name": name, "privacy": privacy})

    def create_channel(self, name: str, broadcast: bool = False) -> Dict[str, Any]:
        return self._post({"action": "create_channel", "name": name, "is_broadcast": bool(broadcast)})

    def report(self, typ: str, target_id: int, reason: str = "") -> Dict[str, Any]:
        return self._post({"action": "report", "type": typ, "target_id": int(target_id), "reason": reason})

    # ---- session helpers ----
    def sess_save(self, passphrase: str) -> None:
        ck = {c.name: c.value for c in self.s.cookies}
        save_session(ck, passphrase, path=self._session_file)

    def sess_load(self, passphrase: str) -> bool:
        try:
            j = load_session(passphrase, path=self._session_file)
            for k, v in j.get("cookies", {}).items():
                self.s.cookies.set(k, v)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            raise NavaErr("sess_load_failed", details=str(e))

    def sess_rm(self):
        remove_session(path=self._session_file)

    # ---- utility ----
    def whoami(self) -> Dict[str, Any]:
        return self._post({"action": "get_user"})
