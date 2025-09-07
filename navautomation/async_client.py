# navautomation/async_client.py
import httpx, json
from typing import Dict, Any, Optional
from . import config
from .errors import NavaErr, make_err_from_resp
from .session_store import save_session, load_session, remove_session
from .utils import now_iso
from pathlib import Path

class AsyncClient:
    """Client async با متدهای خیلی کوتاه (همون نام‌ها مثل sync)"""
    def __init__(self, base: Optional[str]=None, api_path: Optional[str]=None, timeout:int=12):
        self.base = (base or config.DEFAULT_BASE).rstrip("/")
        self.api = api_path or config.DEFAULT_API_PATH
        self.url = self.base + self.api
        self.client = httpx.AsyncClient(timeout=timeout, headers={"User-Agent":"NavaAsync/0.1"})

    async def _post(self, payload: Dict[str,Any]) -> Dict[str,Any]:
        try:
            r = await self.client.post(self.url, json=payload)
        except Exception as e:
            raise NavaErr("net_error", details=str(e))
        try:
            data = r.json()
        except Exception:
            if r.is_success:
                return {"success": True, "raw": r.text}
            raise NavaErr("bad_response", details=r.text)
        if isinstance(data, dict) and data.get("success") is False:
            raise make_err_from_resp(data)
        return data

    # same short wrappers
    async def otp_send(self, email: str) -> Dict[str,Any]:
        return await self._post({"action":"send_otp","email":email})

    async def otp_ver(self, email: str, code: str) -> Dict[str,Any]:
        return await self._post({"action":"verify_otp","email":email,"code":code})

    async def otp_login(self, email: str, code: str) -> Dict[str,Any]:
        return await self._post({"action":"login_by_otp","email":email,"code":code})

    async def auth_login(self, user: str, pwd: str) -> Dict[str,Any]:
        return await self._post({"action":"login","username":user,"password":pwd})

    async def auth_signup(self, user: str, email: str, pwd: str) -> Dict[str,Any]:
        return await self._post({"action":"signup","username":user,"email":email,"password":pwd})

    async def msg_send(self, tt: str, id: int, body: str) -> Dict[str,Any]:
        return await self._post({"action":"send_message","target_type":tt,"target_id":int(id),"body":body})

    async def msg_fetch(self, tt: str, id: int) -> Dict[str,Any]:
        return await self._post({"action":"fetch_messages","target_type":tt,"target_id":int(id)})

    async def close(self):
        await self.client.aclose()

    # session save/load for async client (saves cookies dict)
    async def sess_save(self, passphrase: str):
        try:
            jar = {c.name:c.value for c in self.client.cookies.jar}
        except Exception:
            jar = dict(self.client.cookies)
        save_session(jar, passphrase, path=None)

    async def sess_load(self, passphrase: str) -> bool:
        try:
            j = load_session(passphrase, path=None)
            self.client.cookies.update(j.get("cookies", {}))
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            raise NavaErr("sess_load_failed", details=str(e))
