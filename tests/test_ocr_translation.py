import os
import base64
from pathlib import Path

from youdaoai import YoudaoAI

youdaoai_client = YoudaoAI(os.getenv("APP_KEY") or "", os.getenv("APP_SECRET") or "")
result = youdaoai_client.ocr_translate(img=Path(__file__).parent / Path("test-img.jpeg"), from_="en", to_="zh-CHS")
print(result)


result = youdaoai_client.ocr_translate(
    img=Path(__file__).parent / Path("test-img.jpeg"), from_="en", to_="zh-CHS", render=True
)

if result.render_image:
    with open("ocr_translated_image.png", "wb") as f:
        f.write(base64.b64decode(result.render_image))
else:
    print("No render image")
