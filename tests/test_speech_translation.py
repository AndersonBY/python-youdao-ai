import os
from pathlib import Path

from youdaoai import YoudaoAI

youdaoai_client = YoudaoAI(os.getenv("APP_KEY") or "", os.getenv("APP_SECRET") or "")
result = youdaoai_client.speech_translate(Path(__file__).parent / Path("test-audio.wav"), "en", "zh-CHS")
print(result)
