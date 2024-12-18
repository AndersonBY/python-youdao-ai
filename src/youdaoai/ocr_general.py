import time
import base64
from pathlib import Path
from typing import Optional, Dict, Union, Any

from .base import Base


class OCRGeneral(Base):
    def _get_base64(self, q: Union[str, Path]) -> str:
        p = Path(q)
        if p.exists():
            with open(q, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        else:
            return str(q)

    def recognize(
        self,
        img: Union[str, Path],
        langType: str = "auto",
        detectType: str = "10012",
        imageType: str = "1",
        angle: Optional[str] = None,
        column: Optional[str] = None,
        rotate: Optional[str] = None,
    ) -> Dict[str, Any]:
        data: Dict[str, str] = {}
        data["img"] = self._get_base64(img)
        data["langType"] = langType
        data["detectType"] = detectType
        data["imageType"] = imageType
        data["signType"] = "v3"
        data["curtime"] = str(int(time.time()))
        data["salt"] = self._get_salt()
        data["appKey"] = self.app_key
        data["sign"] = self._get_sign(data["img"], data["salt"], data["curtime"])

        if angle:
            data["angle"] = angle
        if column:
            data["column"] = column
        if rotate:
            data["rotate"] = rotate

        response = self._do_request("ocrapi", data)
        return response.json()
