import wave
import base64
from pathlib import Path
from typing import Dict, Union, Any

from .base import Base


class SpeechTranslation(Base):
    def _get_base64(self, q: Union[str, Path]) -> str:
        audio_file_path = Path(q)
        extension = audio_file_path.suffix.lower()
        if extension != ".wav":
            raise TypeError("Unsupported audio format")

        with open(audio_file_path, "rb") as file_wav:
            return base64.b64encode(file_wav.read()).decode("utf-8")

    def _get_audio_info(self, audio_file_path: Union[str, Path]) -> Dict[str, int]:
        with wave.open(str(audio_file_path), "rb") as wav_info:
            sample_rate = wav_info.getframerate()
            nchannels = wav_info.getnchannels()

        return {"sample_rate": sample_rate, "nchannels": nchannels}

    def translate(
        self,
        q: Union[str, Path],
        from_: str,
        to_: str,
        rate: Union[str, int] = "auto",
        format_: str = "wav",
        channel: str = "1",
        type_: str = "1",
        ext: str = "mp3",
        voice: str = "0",
        signType: str = "v1",
        version: str = "v1",
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        data["q"] = self._get_base64(q)
        data["from"] = from_
        data["to"] = to_
        data["rate"] = rate if rate != "auto" else self._get_audio_info(q)["sample_rate"]
        data["format"] = format_
        data["channel"] = channel
        data["type"] = type_
        data["ext"] = ext
        data["voice"] = voice
        data["signType"] = signType
        data["version"] = version
        data["salt"] = self._get_salt()
        data["appKey"] = self.app_key
        data["sign"] = self._get_sign(data["q"], data["salt"], truncate=False, method="md5")

        response = self._do_request("speechtransapi", data)
        return response.json()
