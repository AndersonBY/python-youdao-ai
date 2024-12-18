import os

from youdaoai import Translation


ts = Translation(os.getenv("APP_KEY") or "", os.getenv("APP_SECRET") or "")
result = ts.translate("大家好我是毕老师", "zh-CHS", "en")
print(result)
