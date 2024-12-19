import uuid
import time
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, Union, Literal, overload

import httpx

from .types import (
    TranslationResponse,
    SpeechTranslationResponse,
    ASRResponse,
    OCRResponse,
    OCRTableExcelResponse,
    OCRTableJsonResponse,
    OCRTranslateResponse,
    TTSResponse,
    YoudaoError,
)
from ._utils import _get_base64, _get_audio_info


class BaseClient:
    def __init__(self, app_key: str, app_secret: str, base_url: str = "https://openapi.youdao.com/") -> None:
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = base_url

    def _encrypt(self, sign_str: str, method: str = "sha256") -> str:
        if method == "sha256":
            hash_algorithm = hashlib.sha256()
        elif method == "md5":
            hash_algorithm = hashlib.md5()
        else:
            raise ValueError(f"Invalid method: {method}")
        hash_algorithm.update(sign_str.encode("utf-8"))
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

    def _update_payload(self, payload: Dict[str, Any], sign_key: str = "q") -> Dict[str, Any]:
        payload["signType"] = "v3"
        payload["curtime"] = str(int(time.time()))
        payload["salt"] = self._get_salt()
        payload["appKey"] = self.app_key
        payload["sign"] = self._get_sign(payload[sign_key], payload["salt"], payload["curtime"])
        return payload


class YoudaoAI(BaseClient):
    def _do_request(self, api_path: str, data: dict) -> httpx.Response:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = httpx.post(self.base_url + api_path, data=data, headers=headers)
        if int(response.json().get("errorCode", 0)) != 0:
            raise YoudaoError(response.json())
        return response

    def translate(
        self,
        text: str,
        from_: str,
        to_: str,
        ext: Optional[str] = None,
        voice: Optional[str] = None,
        strict: Optional[bool] = None,
        domain: Optional[str] = None,
        vocab_id: Optional[str] = None,
    ) -> TranslationResponse:
        data: Dict[str, Any] = {}
        data["q"] = text
        data["from"] = from_
        data["to"] = to_
        data = self._update_payload(data)

        if ext:
            data["ext"] = ext
        if voice:
            data["voice"] = voice
        if strict:
            data["strict"] = strict
        if vocab_id:
            data["vocabId"] = vocab_id
        if domain:
            data["domain"] = domain

        response = self._do_request("api", data)
        return TranslationResponse(**response.json())

    def speech_translate(
        self,
        audio_file_path: Union[str, Path],
        from_: str,
        to_: str,
        rate: Union[str, int] = "auto",
        format_: str = "wav",
        channel: int = 1,
        type_: int = 1,
        ext: str = "mp3",
        voice: int = 0,
        version: str = "v1",
    ) -> SpeechTranslationResponse:
        data: Dict[str, Any] = {}
        data["q"] = _get_base64(audio_file_path)
        data["from"] = from_
        data["to"] = to_
        data["rate"] = rate if rate != "auto" else _get_audio_info(audio_file_path)["sample_rate"]
        data["format"] = format_
        data["channel"] = channel
        data["type"] = type_
        data["ext"] = ext
        data["voice"] = voice
        data["version"] = version
        data = self._update_payload(data)

        response = self._do_request("speechtransapi", data)
        return SpeechTranslationResponse(**response.json())

    def asr(
        self,
        audio_file_path: Union[str, Path],
        lang_type: str,
        rate: Union[str, int] = "auto",
        format_: str = "wav",
        channel: int = 1,
    ) -> ASRResponse:
        data: Dict[str, str] = {}
        data["q"] = _get_base64(audio_file_path)
        data["langType"] = lang_type
        data["rate"] = str(rate) if rate != "auto" else str(_get_audio_info(audio_file_path)["sample_rate"])
        data["format"] = str(format_)
        data["channel"] = str(channel)
        data["type"] = "1"
        data = self._update_payload(data)

        response = self._do_request("asrapi", data)
        return ASRResponse(**response.json())

    def ocr_general(
        self,
        *,
        img: Optional[Union[str, Path]] = None,
        img_base64: Optional[str] = None,
        lang_type: str = "auto",
        detect_type: str = "10012",
        image_type: str = "1",
        angle: Optional[str] = None,
        column: Optional[str] = None,
        rotate: Optional[str] = None,
    ) -> OCRResponse:
        data: Dict[str, str] = {}
        if img:
            data["img"] = _get_base64(img)
        elif img_base64:
            data["img"] = img_base64
        else:
            raise ValueError("img or img_base64 is required")
        data["langType"] = lang_type
        data["detectType"] = detect_type
        data["imageType"] = image_type
        data = self._update_payload(data, sign_key="img")

        if angle:
            data["angle"] = angle
        if column:
            data["column"] = column
        if rotate:
            data["rotate"] = rotate

        response = self._do_request("ocrapi", data)
        return OCRResponse(**response.json())

    @overload
    def ocr_table(
        self,
        *,
        img: Optional[Union[str, Path]] = None,
        img_base64: Optional[str] = None,
        doc_type: Literal["json"],
        angle: Optional[int] = None,
    ) -> OCRTableJsonResponse: ...

    @overload
    def ocr_table(
        self,
        *,
        img: Optional[Union[str, Path]] = None,
        img_base64: Optional[str] = None,
        doc_type: Literal["excel"] = "excel",
        angle: Optional[int] = None,
    ) -> OCRTableExcelResponse: ...

    def ocr_table(
        self,
        *,
        img: Optional[Union[str, Path]] = None,
        img_base64: Optional[str] = None,
        doc_type: Union[Literal["json"], Literal["excel"]] = "excel",
        angle: Optional[int] = None,
    ) -> Union[OCRTableExcelResponse, OCRTableJsonResponse]:
        data: Dict[str, str] = {}
        if img:
            data["q"] = _get_base64(img)
        elif img_base64:
            data["q"] = img_base64
        else:
            raise ValueError("img or img_base64 is required")
        data["type"] = "1"
        data["docType"] = doc_type
        data = self._update_payload(data)

        if angle:
            data["angle"] = str(angle)

        response = self._do_request("ocr_table", data)
        if doc_type == "json":
            return OCRTableJsonResponse(**response.json())
        elif doc_type == "excel":
            return OCRTableExcelResponse(**response.json())
        else:
            raise ValueError(f"Invalid doc_type: {doc_type}")

    def ocr_translate(
        self,
        *,
        img: Optional[Union[str, Path]] = None,
        img_base64: Optional[str] = None,
        from_: str,
        to_: str,
        ext: Optional[str] = None,
        render: Optional[bool] = None,
    ) -> OCRTranslateResponse:
        data: Dict[str, Any] = {}
        if img:
            data["q"] = _get_base64(img)
        elif img_base64:
            data["q"] = img_base64
        else:
            raise ValueError("img or img_base64 is required")
        data["from"] = from_
        data["to"] = to_
        data["type"] = "1"
        data = self._update_payload(data)

        if ext:
            data["ext"] = ext
        if render is not None:
            data["render"] = 1 if render else 0

        response = self._do_request("ocrtransapi", data)
        with open("ocr_translate_response.json", "w", encoding="utf-8") as f:
            f.write(response.text)
        return OCRTranslateResponse(**response.json())

    def tts(
        self,
        text: str,
        speed: int = 1,
        volumn: float = 1.0,
        voice: str = "youxiaoqin",
    ) -> Union[TTSResponse, bytes]:
        data: Dict[str, str] = {}
        data["q"] = text
        data["speed"] = str(speed)
        data["volumn"] = str(volumn)
        data["voiceName"] = str(voice)
        data = self._update_payload(data)

        response = self._do_request("ttsapi", data)
        if response.headers["Content-Type"] == "audio/mp3":
            return response.content
        else:
            return TTSResponse(**response.json())


class AsyncYoudaoAI(BaseClient):
    async def _do_request(self, api_path: str, data: dict) -> httpx.Response:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url + api_path, data=data, headers=headers)
            if int(response.json().get("errorCode", 0)) != 0:
                raise YoudaoError(response.json())
            return response

    async def translate(
        self,
        text: str,
        from_: str,
        to_: str,
        ext: Optional[str] = None,
        voice: Optional[str] = None,
        strict: Optional[bool] = None,
        domain: Optional[str] = None,
        vocab_id: Optional[str] = None,
    ) -> TranslationResponse:
        data: Dict[str, Any] = {}
        data["q"] = text
        data["from"] = from_
        data["to"] = to_
        data = self._update_payload(data)

        if ext:
            data["ext"] = ext
        if voice:
            data["voice"] = voice
        if strict:
            data["strict"] = strict
        if vocab_id:
            data["vocabId"] = vocab_id
        if domain:
            data["domain"] = domain

        response = await self._do_request("api", data)
        return TranslationResponse(**response.json())

    async def speech_translate(
        self,
        audio_file_path: Union[str, Path],
        from_: str,
        to_: str,
        rate: Union[str, int] = "auto",
        format_: str = "wav",
        channel: int = 1,
        type_: int = 1,
        ext: str = "mp3",
        voice: int = 0,
        version: str = "v1",
    ) -> SpeechTranslationResponse:
        data: Dict[str, Any] = {}
        data["q"] = _get_base64(audio_file_path)
        data["from"] = from_
        data["to"] = to_
        data["rate"] = rate if rate != "auto" else _get_audio_info(audio_file_path)["sample_rate"]
        data["format"] = format_
        data["channel"] = channel
        data["type"] = type_
        data["ext"] = ext
        data["voice"] = voice
        data["version"] = version
        data = self._update_payload(data)

        response = await self._do_request("speechtransapi", data)
        return SpeechTranslationResponse(**response.json())

    async def asr(
        self,
        audio_file_path: Union[str, Path],
        lang_type: str,
        rate: Union[str, int] = "auto",
        format_: str = "wav",
        channel: int = 1,
    ) -> ASRResponse:
        data: Dict[str, str] = {}
        data["q"] = _get_base64(audio_file_path)
        data["langType"] = lang_type
        data["rate"] = str(rate) if rate != "auto" else str(_get_audio_info(audio_file_path)["sample_rate"])
        data["format"] = str(format_)
        data["channel"] = str(channel)
        data["type"] = "1"
        data = self._update_payload(data)

        response = await self._do_request("asrapi", data)
        return ASRResponse(**response.json())

    async def ocr_general(
        self,
        *,
        img: Optional[Union[str, Path]] = None,
        img_base64: Optional[str] = None,
        lang_type: str = "auto",
        detect_type: str = "10012",
        image_type: str = "1",
        angle: Optional[str] = None,
        column: Optional[str] = None,
        rotate: Optional[str] = None,
    ) -> OCRResponse:
        data: Dict[str, str] = {}
        if img:
            data["img"] = _get_base64(img)
        elif img_base64:
            data["img"] = img_base64
        else:
            raise ValueError("img or img_base64 is required")
        data["langType"] = lang_type
        data["detectType"] = detect_type
        data["imageType"] = image_type
        data = self._update_payload(data, sign_key="img")

        if angle:
            data["angle"] = angle
        if column:
            data["column"] = column
        if rotate:
            data["rotate"] = rotate

        response = await self._do_request("ocrapi", data)
        return OCRResponse(**response.json())

    @overload
    async def ocr_table(
        self,
        *,
        img: Optional[Union[str, Path]] = None,
        img_base64: Optional[str] = None,
        doc_type: Literal["json"],
        angle: Optional[int] = None,
    ) -> OCRTableJsonResponse: ...

    @overload
    async def ocr_table(
        self,
        *,
        img: Optional[Union[str, Path]] = None,
        img_base64: Optional[str] = None,
        doc_type: Literal["excel"] = "excel",
        angle: Optional[int] = None,
    ) -> OCRTableExcelResponse: ...

    async def ocr_table(
        self,
        *,
        img: Optional[Union[str, Path]] = None,
        img_base64: Optional[str] = None,
        doc_type: Union[Literal["json"], Literal["excel"]] = "excel",
        angle: Optional[int] = None,
    ) -> Union[OCRTableExcelResponse, OCRTableJsonResponse]:
        data: Dict[str, str] = {}
        if img:
            data["q"] = _get_base64(img)
        elif img_base64:
            data["q"] = img_base64
        else:
            raise ValueError("img or img_base64 is required")
        data["type"] = "1"
        data["docType"] = doc_type
        data = self._update_payload(data)

        if angle:
            data["angle"] = str(angle)

        response = await self._do_request("ocr_table", data)
        if doc_type == "json":
            return OCRTableJsonResponse(**response.json())
        elif doc_type == "excel":
            return OCRTableExcelResponse(**response.json())
        else:
            raise ValueError(f"Invalid doc_type: {doc_type}")

    async def ocr_translate(
        self,
        *,
        img: Optional[Union[str, Path]] = None,
        img_base64: Optional[str] = None,
        from_: str,
        to_: str,
        ext: Optional[str] = None,
        render: Optional[bool] = None,
    ) -> OCRTranslateResponse:
        data: Dict[str, Any] = {}
        if img:
            data["q"] = _get_base64(img)
        elif img_base64:
            data["q"] = img_base64
        else:
            raise ValueError("img or img_base64 is required")
        data["from"] = from_
        data["to"] = to_
        data["type"] = "1"
        data = self._update_payload(data)

        if ext:
            data["ext"] = ext
        if render is not None:
            data["render"] = 1 if render else 0

        response = await self._do_request("ocrtransapi", data)
        with open("ocr_translate_response.json", "w", encoding="utf-8") as f:
            f.write(response.text)
        return OCRTranslateResponse(**response.json())

    async def tts(
        self,
        text: str,
        speed: int = 1,
        volumn: float = 1.0,
        voice: str = "youxiaoqin",
    ) -> Union[TTSResponse, bytes]:
        data: Dict[str, str] = {}
        data["q"] = text
        data["speed"] = str(speed)
        data["volumn"] = str(volumn)
        data["voiceName"] = str(voice)
        data = self._update_payload(data)

        response = await self._do_request("ttsapi", data)
        if response.headers["Content-Type"] == "audio/mp3":
            return response.content
        else:
            return TTSResponse(**response.json())
