# python-youdao-ai
[有道智云](https://ai.youdao.com)API的Python SDK。

## 安装

```
pip install youdaoai
```

## 使用方法

同步客户端

```Python
from youdaoai import YoudaoAI

# 创建有道智云客户端
client = YoudaoAI('你的APP_KEY', '你的APP_SECRET')

result = client.translate('今天天气真不错', 'zh-CHS', 'en')
print(result)
```

异步客户端

```Python
import asyncio
from youdaoai import AsyncYoudaoAI

# 创建有道智云客户端
client = AsyncYoudaoAI('你的APP_KEY', '你的APP_SECRET')

async def main():
    result = await client.translate('今天天气真不错', 'zh-CHS', 'en')
    print(result)

if __name__ == '__main__':
    asyncio.run(main())
```

#### [文本翻译服务](https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html)

| 参数			| 默认值			| 描述			|
| ------------- | ------------- | ------------- |
| q				| 无，必填		| 待翻译文本		|
| from_			| 无，必填		| 源语言			|
| to_			| 无，必填		| 目标语言		|
| ext			| None			| 翻译结果音频格式，支持mp3 |
| audio_path	| None			| 音频储存路径 |
| voice			| None			| 翻译结果发音选择，0为女声，1为男声 |
| strict		| None			| 是否严格按照指定from和to进行翻译：true/false |
| vocabId		| None			| 用户上传的词典 |

```Python
from youdaoai import Youdao

# 创建有道智云客户端
client = Youdao('你的APP_KEY', '你的APP_SECRET')

# 中文翻译为英文
result = await client.translate(
    q='今天天气真不错',
    from_='zh-CHS',
    to_='en'
)
print(result)
```

#### [图片翻译服务](https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E5%9B%BE%E7%89%87%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E5%9B%BE%E7%89%87%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html)

| 参数			| 默认值			| 描述			|
| ------------- | ------------- | ------------- |
| q				| 无，必填		| 待翻译文本		|
| from_			| 无，必填		| 源语言			|
| to_			| 无，必填		| 目标语言		|
| ext			| None			| 翻译结果音频格式，支持mp3 |
| audio_path	| None			| 音频储存路径 |
| docType		| None			| 服务器响应类型，目前只支持json |
| render		| None			| 是否需要服务端返回渲染的图片，0：否；1：是，默认是0 |
| nullIsError	| None			| 如果ocr没有检测到文字，是否返回错误，false：否；true：是，默认是false |

```Python
from youdaoai import Youdao

# 创建有道智云客户端
client = Youdao('你的APP_KEY', '你的APP_SECRET')

result = client.ocr_translate(img=Path(__file__).parent / Path("test-img.jpeg"), from_="en", to_="zh-CHS")
print(result)

result = client.ocr_translate(
    img=Path(__file__).parent / Path("test-img.jpeg"), from_="en", to_="zh-CHS", render=True
)

if result.render_image:
    with open("ocr_translated_image.png", "wb") as f:
        f.write(base64.b64decode(result.render_image))
else:
    print("No render image")

```

#### [语音翻译服务](https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E8%AF%AD%E9%9F%B3%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E8%AF%AD%E9%9F%B3%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html)

| 参数			| 默认值			| 描述			|
| ------------- | ------------- | ------------- |
| q				| 无，必填		| 待翻译文本		|
| from_			| 无，必填		| 源语言			|
| to_			| 无，必填		| 目标语言		|
| rate			| 'auto'		| 采样率，默认会自动分析 |
| format_		| 'wav'			| 语音文件的格式， 目前只支持wav |
| channel		| '1'			| 声道数， 仅支持单声道，请填写固定值1 |
| type_			| '1'			| 上传类型， 仅支持Base64上传，请填写固定值1 |
| ext			| 'mp3'			| 翻译结果音频格式，支持mp3，默认mp3 |
| voice			| '0'			| 翻译结果发音选择，0为女声，1为男声 |
| signType		| 'v1'			| 签名版本 |
| version		| 'v1'			| 接口版本 |

```Python
from youdaoai import Youdao

# 创建有道智云客户端
client = Youdao('你的APP_KEY', '你的APP_SECRET')

# 语音文件翻译
result = await client.speech_translate(
    q='speech.wav',
    from_='zh-CHS',
    to_='en',
    rate='16000',  # 采样率
    voice='0'      # 0为女声，1为男声
)
print(result)
```

#### [通用文字识别服务](https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html)

| 参数			| 默认值			| 描述			|
| ------------- | ------------- | ------------- |
| img			| 无，必填		| 待识别图像路径		|
| langType		| 'auto'		| 要识别的语言类型	|
| angle			| None	| 是否进行360角度识别，0：不识别，1：识别。默认不识别（0） |
| column		| None	| 是否按多列识别，onecolumn：按单列识别；columns：按多列识别。默认按单列识别 |
| rotate		| None	| 是否需要获得文字旋转角度，donot_rotate：不需要得到倾斜角度，rotate：得到倾斜角度。默认不需要 |

```Python
from youdaoai import Youdao

# 创建有道智云客户端
client = Youdao('你的APP_KEY', '你的APP_SECRET')

# OCR通用文字识别
result = await client.ocr_general(
    img='test_image.png',
    langType='zh-CHS',
    angle=1,        # 启用360度识别
    column='columns' # 按多列识别
)
print(result)
```

#### [表格OCR服务](https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E8%A1%A8%E6%A0%BCOCR%E6%9C%8D%E5%8A%A1/%E8%A1%A8%E6%A0%BCOCR%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html)

| 参数			| 默认值			| 描述			|
| ------------- | ------------- | ------------- |
| img			| 无，必填	| 待识别图像路径		|
| docType		| 无，必填	| 服务器响应类型，目前支持json和Excel	|
| excel_filepath | None		| 若docType为excel可通过该参数指定生成的xlsx文件路径，若不填该参数则不会生成xlsx文件|
| angle			| None		| 是否进行360角度识别，0：不识别，1：识别。默认不识别（0） |

```Python
from youdaoai import Youdao

# 创建有道智云客户端
client = Youdao('你的APP_KEY', '你的APP_SECRET')

# 表格OCR识别
result = await client.ocr_table(
    img='表格图片.jpg',
    docType='excel',
    excel_filepath='test.xlsx'
)
print(result)
```

#### [语音合成服务](https://ai.youdao.com/DOCSIRMA/html/%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90TTS/API%E6%96%87%E6%A1%A3/%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90%E6%9C%8D%E5%8A%A1/%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html)

| 参数			| 默认值			| 描述			|
| ------------- | ------------- | ------------- |
| q				| 无，必填	| 待合成音频文件的文本字符串 |
| langType		| 无，必填	| 合成文本的语言类型 |
| filepath		| 无，必填	| 指定生成的mp3文件路径 |
| voice			| 0			| 翻译结果发音选择，0为女声，1为男声，默认为女声 |
| speed			| 1			| 合成音频的语速，1为正常速度，最大为2，最小为0.1 |
| volumn		| 1			| 合成音频的音量，正常为1.00，最大为5.00，最小为0.50 |

```Python
from youdaoai import Youdao

# 创建有道智云客户端
client = Youdao('你的APP_KEY', '你的APP_SECRET')

# 基础语音合成
result = await client.tts(
    q='你好，世界',
    langType='zh-CHS',
    filepath='output.mp3'
)
print(result)
```


#### [短语音识别服务](https://ai.youdao.com/DOCSIRMA/html/%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%ABASR/API%E6%96%87%E6%A1%A3/%E7%9F%AD%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E7%9F%AD%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html)

| 参数			| 默认值			| 描述			|
| ------------- | ------------- | ------------- |
| q				| 无，必填		| 待合成音频文件的文本字符串 |
| langType		| 无，必填		| 合成文本的语言类型，详情见官方文档 |
| rate			| 'auto'		| 采样率，默认会自动分析（仅支持分析wav格式），非wav格式请手动指定采样率 |
| format_		| 'wav'			| 语音文件的格式， 目前支持wav、aac、mp3 |
| channel		| '1'			| 声道数， 仅支持单声道，请填写固定值1 |

```Python
from youdaoai import Youdao

# 创建有道智云客户端
client = Youdao('你的APP_KEY', '你的APP_SECRET')

# WAV文件识别
result = await client.asr(
    q='speech.wav',
    langType='zh-CHS'
)
print(result)
```
