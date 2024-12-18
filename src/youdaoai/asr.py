import wave
import time
import base64
from pathlib import Path
from typing import Dict, Union, Any

from .base import Base


class ASR(Base):
    def _get_base64(self, q: Union[str, Path]) -> str:
        audio_file_path = Path(q)
        extension = audio_file_path.suffix.lower()
        if extension not in (".wav", ".aac", ".mp3"):
            raise TypeError("Unsupported audio format")

        with open(audio_file_path, "rb") as file_wav:
            return base64.b64encode(file_wav.read()).decode("utf-8")

    def _get_audio_info(self, audio_file_path_str: Union[str, Path]) -> Dict[str, int]:
        audio_file_path = Path(audio_file_path_str)
        extension = audio_file_path.suffix.lower()
        if extension != ".wav":
            raise TypeError("Please manually specify sample rate for non-WAV audio")

        with wave.open(str(audio_file_path_str), "rb") as wav_info:
            sample_rate = wav_info.getframerate()
            nchannels = wav_info.getnchannels()

        return {"sample_rate": sample_rate, "nchannels": nchannels}

    def recognize(
        self,
        q: Union[str, Path],
        langType: str,
        rate: Union[str, int] = "auto",
        format_: str = "wav",
        channel: str = "1",
    ) -> Dict[str, Any]:
        data: Dict[str, str] = {}
        data["q"] = self._get_base64(q)
        data["langType"] = langType
        data["rate"] = str(rate) if rate != "auto" else str(self._get_audio_info(q)["sample_rate"])
        data["curtime"] = str(int(time.time()))
        data["format"] = str(format_)
        data["channel"] = str(channel)
        data["signType"] = "v2"
        data["type"] = "1"
        data["salt"] = self._get_salt()
        data["appKey"] = self.app_key
        data["sign"] = self._get_sign(data["q"], data["salt"], data["curtime"])

        response = self._do_request("asrapi", data)
        return response.json()
