import os
from pathlib import Path

from youdaoai import YoudaoAI

youdaoai_client = YoudaoAI(os.getenv("APP_KEY") or "", os.getenv("APP_SECRET") or "")
result = youdaoai_client.asr(Path(__file__).parent / Path("test-audio.wav"), "en")
print(result)
