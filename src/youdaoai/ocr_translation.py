import time
import os
import base64
from pathlib import Path
from typing import Optional, Union, Dict, Any

from .base import Base


class OCRTranslation(Base):
    def _get_base64(self, q: Union[str, Path]) -> str:
        p = Path(q)
        if p.exists():
            with open(q, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        else:
            return str(q)

    def translate(
        self,
        q: Union[str, Path],
        from_: str,
        to_: str,
        ext: Optional[str] = None,
        audio_path: Optional[str] = None,
        docType: Optional[str] = None,
        render: Optional[bool] = None,
        nullIsError: Optional[bool] = None,
    ) -> Union[bool, Dict[str, Any]]:
        data: Dict[str, Any] = {}
        data["q"] = self._get_base64(q)
        data["from"] = from_
        data["to"] = to_
        data["type"] = "1"
        data["salt"] = self._get_salt()
        data["appKey"] = self.app_key
        data["sign"] = self._get_sign(data["q"], data["salt"], truncate=False, method="md5")

        if ext:
            data["ext"] = ext
        if not audio_path:
            audio_path = os.path.join(os.getcwd(), str(int(round(time.time() * 1000))) + ".mp3")
        if docType:
            data["docType"] = docType
        if render:
            data["render"] = render
        if nullIsError:
            data["nullIsError"] = nullIsError

        response = self._do_request("ocrtransapi", data)
        contentType = response.headers["Content-Type"]
        if contentType == "audio/mp3":
            with open(audio_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            return response.json()
