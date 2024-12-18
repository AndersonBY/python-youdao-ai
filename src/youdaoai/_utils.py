import wave
import base64
from pathlib import Path
from typing import Union, Dict


def _get_base64(q: Union[str, Path]) -> str:
    p = Path(q)
    if p.exists():
        with open(q, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    else:
        return str(q)


def _get_audio_info(audio_file_path: Union[str, Path]) -> Dict[str, int]:
    with wave.open(str(audio_file_path), "rb") as wav_info:
        sample_rate = wav_info.getframerate()
        nchannels = wav_info.getnchannels()

    return {"sample_rate": sample_rate, "nchannels": nchannels}
