import os
import time
from pathlib import Path
from typing import Union, Dict, Any, Optional

from .base import Base


class Translation(Base):
    def translate(
        self,
        q: str,
        from_: str,
        to_: str,
        ext: Optional[str] = None,
        audio_path: Optional[Union[str, Path]] = None,
        voice: Optional[str] = None,
        strict: Optional[bool] = None,
        vocabId: Optional[str] = None,
    ) -> Union[Dict[str, Any], bool]:
        data: Dict[str, Any] = {}
        data["q"] = q
        data["from"] = from_
        data["to"] = to_
        data["signType"] = "v3"
        data["curtime"] = str(int(time.time()))
        data["salt"] = self._get_salt()
        data["appKey"] = self.app_key
        data["sign"] = self._get_sign(q, data["salt"], data["curtime"])

        if ext:
            data["ext"] = ext
        if not audio_path:
            audio_path = Path(os.getcwd()) / f"{int(round(time.time() * 1000))}.mp3"
        if voice:
            data["voice"] = voice
        if strict:
            data["strict"] = strict
        if vocabId:
            data["vocabId"] = vocabId

        response = self._do_request("api", data)
        contentType = response.headers["Content-Type"]
        if contentType == "audio/mp3":
            with open(audio_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            return response.json()
