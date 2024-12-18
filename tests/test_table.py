import os
import base64
from pathlib import Path

from youdaoai import YoudaoAI

youdaoai_client = YoudaoAI(os.getenv("APP_KEY") or "", os.getenv("APP_SECRET") or "")
result = youdaoai_client.ocr_table(img=Path(__file__).parent / Path("test-table1.jpg"), doc_type="json")
print(result)

result = youdaoai_client.ocr_table(
    img=Path(__file__).parent / Path("test-table2.png"),
)
if result.result and result.result:
    with open(Path(__file__).parent / Path("test-table2.xlsx"), "wb") as f:
        f.write(base64.b64decode(result.result.tables[0].encode("utf-8")))
