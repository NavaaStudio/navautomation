# navautomation/errors.py
from typing import Optional, Any, Dict
import traceback

class NavaErr(Exception):
    """ساختار خطا برای کار با نوا — شبیه aiobale: code/message/details/resp"""
    def __init__(self, msg: str = "nava_error", code: Optional[str]=None, details: Optional[str]=None, resp: Optional[Any]=None):
        super().__init__(msg)
        self.code = code
        self.details = details
        self.resp = resp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": str(self),
            "code": self.code,
            "details": self.details,
            "resp": self.resp,
        }

def make_err_from_resp(resp: Any) -> NavaErr:
    """اگر actions.php شکل JSON خطا برگردونه، اینو تبدیل کن."""
    try:
        if isinstance(resp, dict):
            if resp.get("success") is False:
                return NavaErr(str(resp.get("message") or resp.get("error") or "server_error"),
                               code=resp.get("error"),
                               details=resp.get("detail") or resp.get("exception"),
                               resp=resp)
    except Exception:
        pass
    return NavaErr("server_error", details=str(resp), resp=resp)

def make_err(msg: str, code: Optional[str]=None, details: Optional[str]=None):
    return NavaErr(msg, code=code, details=details)
