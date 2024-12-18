import uuid
import httpx
import hashlib
from typing import Optional


YOUDAO_URL: str = "https://openapi.youdao.com/"


class Base:
    def __init__(self, app_key: str, app_secret: str) -> None:
        self.app_key = app_key
        self.app_secret = app_secret

    def _encrypt(self, signStr: str, method: str = "sha256") -> str:
        if method == "sha256":
            hash_algorithm = hashlib.sha256()
        elif method == "md5":
            hash_algorithm = hashlib.md5()
        else:
            raise ValueError(f"Invalid method: {method}")
        hash_algorithm.update(signStr.encode("utf-8"))
        return hash_algorithm.hexdigest()

    def _truncate(self, q: Optional[str]) -> Optional[str]:
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10 : size]

    def _get_salt(self) -> str:
        return str(uuid.uuid1())

    def _get_sign(self, q: str, salt: str, curtime: str = "", truncate: bool = True, method: str = "sha256") -> str:
        if self.app_key is None or self.app_secret is None:
            raise ValueError("app_key or app_secret is None")
        if truncate:
            _truncate = self._truncate(q)
            if _truncate is None:
                raise ValueError("q is None")
            signStr = self.app_key + _truncate + salt + curtime + self.app_secret
        else:
            signStr = self.app_key + q + salt + curtime + self.app_secret
        return self._encrypt(signStr, method)

    def _do_request(self, api_path: str, data: dict) -> httpx.Response:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return httpx.post(YOUDAO_URL + api_path, data=data, headers=headers)
