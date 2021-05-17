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

#### [通用文字识别服务](https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html)

| 参数			| 默认值			| 描述			|
| ------------- | ------------- | ------------- |
| img			| 无，必填		| 待识别图像路径		|
| langType		| 'auto'		| 要识别的语言类型	|
| angle			| None	| 是否进行360角度识别，0：不识别，1：识别。默认不识别（0） |
| column		| None	| 是否按多列识别，onecolumn：按单列识别；columns：按多列识别。默认按单列识别 |
| rotate		| None	| 是否需要获得文字旋转角度，donot_rotate：不需要得到倾斜角度，rotate：得到倾斜角度。默认不需要 |

```Python
from youdaoai import OCRGeneral


ocr = OCRGeneral('你的APP_KEY', '你的APP_SECRET')
result = ocr.recognize('ocr_general.png')
print(result)
```

#### [身份证识别服务](https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E9%80%9A%E7%94%A8%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html)

| 参数			| 默认值			| 描述			|
| ------------- | ------------- | ------------- |
| img			| 无，必填		| 待识别图像路径		|

```Python
from youdaoai import OCRIDCard


ocr = OCRIDCard('你的APP_KEY', '你的APP_SECRET')
result = ocr.recognize('身份证.jpg')
print(result)
```

#### [购物小票识别服务](https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E8%B4%AD%E7%89%A9%E5%B0%8F%E7%A5%A8%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E8%B4%AD%E7%89%A9%E5%B0%8F%E7%A5%A8%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html)

| 参数			| 默认值			| 描述			|
| ------------- | ------------- | ------------- |
| img			| 无，必填		| 待识别图像路径		|

```Python
from youdaoai import OCRReceipt


ocr = OCRReceipt('你的APP_KEY', '你的APP_SECRET')
result = ocr.recognize('购物小票.jpg')
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
from youdaoai import OCRTable


ocr = OCRTable('你的APP_KEY', '你的APP_SECRET')
result = ocr.recognize('表格图片.jpg', 'excel', 'test.xlsx')
print(result)
```

#### [名片识别服务](https://ai.youdao.com/DOCSIRMA/html/%E6%96%87%E5%AD%97%E8%AF%86%E5%88%ABOCR/API%E6%96%87%E6%A1%A3/%E5%90%8D%E7%89%87%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1/%E5%90%8D%E7%89%87%E8%AF%86%E5%88%AB%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html)

| 参数			| 默认值			| 描述			|
| ------------- | ------------- | ------------- |
| img			| 无，必填		| 待识别图像路径		|

```Python
from youdaoai import OCRNamecard


ocr = OCRNamecard('你的APP_KEY', '你的APP_SECRET')
result = ocr.recognize('名片照片.jpg')
print(result)
```