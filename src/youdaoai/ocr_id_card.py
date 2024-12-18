import time
import base64
from pathlib import Path
from typing import Dict, Union

from .base import Base


class OCRIDCard(Base):
    def _get_base64(self, q: Union[str, Path]) -> str:
        p = Path(q)
        if p.exists():
            with open(q, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        else:
            return str(q)

    def recognize(self, img: Union[str, Path], structureType: str = "idcard", docType: str = "json") -> Dict:
        data: Dict[str, str] = {}
        data["q"] = self._get_base64(img)
        data["structureType"] = structureType
        data["docType"] = docType
        data["signType"] = "v3"
        data["curtime"] = str(int(time.time()))
        data["salt"] = self._get_salt()
        data["appKey"] = self.app_key
        data["sign"] = self._get_sign(data["q"], data["salt"], data["curtime"])

        response = self._do_request("ocr_structure", data)
        return response.json()
