import os
import asyncio

from youdaoai import AsyncYoudaoAI


async def main():
    youdaoai_client = AsyncYoudaoAI(os.getenv("APP_KEY") or "", os.getenv("APP_SECRET") or "")
    result = await youdaoai_client.translate("大家好我是毕老师", "zh-CHS", "en")
    print(result)
    print(result.translation[0])


if __name__ == "__main__":
    asyncio.run(main())
