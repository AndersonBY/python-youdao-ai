import os

from youdaoai import YoudaoAI

youdaoai_client = YoudaoAI(os.getenv("APP_KEY") or "", os.getenv("APP_SECRET") or "")
result = youdaoai_client.tts("Hello, world!", speed=1, volumn=1.0, voice="youxiaoqin")

if isinstance(result, bytes):
    with open("tts_result.mp3", "wb") as f:
        f.write(result)
else:
    print(result)
