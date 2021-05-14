# python-youdao-ai
[有道智云](https://ai.youdao.com)API的Python SDK。

## 安装

```
pip install youdaoai
```

## 使用方法

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
from youdaoai import Translation


ts = Translation('你的APP_KEY', '你的APP_SECRET')
result = ts.translate('大家好我是毕老师', 'zh-CHS', 'en')
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
from youdaoai import OCRTranslation


ts = OCRTranslation('你的APP_KEY', '你的APP_SECRET')
result = ts.translate('ocr_translation.png', 'zh-CHS', 'en')
print(result)
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
from youdaoai import SpeechTranslation


ts = SpeechTranslation('你的APP_KEY', '你的APP_SECRET')
result = ts.translate('speech.wav', 'zh-CHS', 'en')
print(result)
```
