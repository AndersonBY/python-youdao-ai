import os
from pathlib import Path

from youdaoai import YoudaoAI

youdaoai_client = YoudaoAI(os.getenv("APP_KEY") or "", os.getenv("APP_SECRET") or "")
result = youdaoai_client.ocr_general(img=Path(__file__).parent / Path("test-img.jpeg"))
print(result)
