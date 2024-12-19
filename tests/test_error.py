import os

from youdaoai import YoudaoAI

youdaoai_client = YoudaoAI(os.getenv("APP_KEY") or "", os.getenv("APP_SECRET") or "")
result = youdaoai_client.translate("大家好我是毕老师", "abc", "123")
print(result)
print(result.translation[0])
