from typing import List, Optional, Union
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """有道API的错误响应类型"""

    error_code: str = Field(alias="errorCode")
    request_id: str = Field(alias="requestId")


class YoudaoError(Exception):
    """有道API的错误"""

    def __init__(self, error_response: dict):
        self.error_response = ErrorResponse(**error_response)
        super().__init__(
            f"Youdao Error: Code: {self.error_response.error_code} - RequestId: {self.error_response.request_id}"
        )


class DictInfo(BaseModel):
    """词典链接信息"""

    url: str


class TranslationResponse(BaseModel):
    """有道翻译API的响应类型"""

    error_code: str = Field(alias="errorCode")
    query: Optional[str] = None
    translation: List[str]
    language_transform: str = Field(alias="l")
    yd_dict: Optional[DictInfo] = Field(None, alias="dict")
    web_dict: Optional[DictInfo] = Field(None, alias="webdict")
    t_speak_url: Optional[str] = Field(None, alias="tSpeakUrl")
    speak_url: Optional[str] = Field(None, alias="speakUrl")
    is_domain_support: Optional[bool] = Field(None, alias="isDomainSupport")

    class Config:
        populate_by_name = True


class SpeechTranslationResponse(BaseModel):
    """有道语音翻译API的响应类型"""

    error_code: str = Field(alias="errorCode")
    query: str
    translation: List[str]
    t_speak_url: str = Field(alias="tSpeakUrl")
    speak_url: str = Field(alias="speakUrl")
    yd_dict: Optional[DictInfo] = Field(None, alias="dict")
    web_dict: Optional[DictInfo] = Field(None, alias="webdict")

    class Config:
        populate_by_name = True


class ASRResponse(BaseModel):
    """有道语音识别API的响应类型"""

    error_code: str = Field(alias="errorCode")
    result: List[str]

    class Config:
        populate_by_name = True


class OCRWord(BaseModel):
    """OCR识别的单个字"""

    bounding_box: str = Field(alias="boundingBox")
    word: str

    class Config:
        populate_by_name = True


class OCRLine(BaseModel):
    """OCR识别的行"""

    bounding_box: str = Field(alias="boundingBox")
    words: List[OCRWord]
    text: str

    class Config:
        populate_by_name = True


class OCRRegion(BaseModel):
    """OCR识别的区域/段落"""

    bounding_box: str = Field(alias="boundingBox")
    dir: str
    lang: str
    lines: List[OCRLine]

    class Config:
        populate_by_name = True


class OCRResult(BaseModel):
    """OCR识别的结果"""

    orientation: str
    regions: List[OCRRegion]


class OCRResponse(BaseModel):
    """有道OCR API的响应类型"""

    error_code: str = Field(alias="errorCode")
    result: Optional[OCRResult] = Field(None, alias="Result")
    msg: Optional[str] = None

    class Config:
        populate_by_name = True


class OCRTableWord(BaseModel):
    """OCR表格识别中的单个字"""

    word: str
    bounding_box: str = Field(alias="boundingBox")

    class Config:
        populate_by_name = True


class OCRTableLine(BaseModel):
    """OCR表格识别中的行"""

    bounding_box: str = Field(alias="boundingBox")
    text: str
    words: List[OCRTableWord]

    class Config:
        populate_by_name = True


class OCRTableCell(BaseModel):
    """OCR表格识别中的单元格"""

    row_range: str = Field(alias="rowRange")
    col_range: str = Field(alias="colRange")
    bounding_box: str = Field(alias="boundingBox")
    dir: str
    lang: str
    lines: List[OCRTableLine]

    class Config:
        populate_by_name = True


class OCRTable(BaseModel):
    """单个表格"""

    cells: List[OCRTableCell]


class OCRTableResult(BaseModel):
    """OCR表格识别结果"""

    orientation: str
    tables: Union[List[OCRTable], List[str]]  # json格式返回OCRTable列表，excel格式返回base64字符串列表


class OCRTableExcelResult(BaseModel):
    """OCR表格识别结果"""

    orientation: str
    tables: List[str]  # excel格式返回base64字符串列表


class OCRTableJsonResult(BaseModel):
    """OCR表格识别结果"""

    orientation: str
    tables: List[OCRTable]  # json格式返回OCRTable列表


class OCRTableExcelResponse(BaseModel):
    """有道OCR表格识别API的响应类型"""

    error_code: str = Field(alias="errorCode")
    result: Optional[OCRTableExcelResult] = Field(None, alias="Result")

    class Config:
        populate_by_name = True


class OCRTableJsonResponse(BaseModel):
    """有道OCR表格识别API的响应类型"""

    error_code: str = Field(alias="errorCode")
    result: Optional[OCRTableJsonResult] = Field(None, alias="Result")

    class Config:
        populate_by_name = True


class OCRTranslateWord(BaseModel):
    """OCR翻译中的单个字"""

    word: Optional[str] = None
    text_height: Optional[float] = Field(None, alias="textHeight")

    class Config:
        populate_by_name = True


class OCRTranslateLine(BaseModel):
    """OCR翻译中的行"""

    text: Optional[str] = None
    words: Optional[List[OCRTranslateWord]] = None


class OCRTranslateRegion(BaseModel):
    """OCR翻译中的区域"""

    bounding_box: str = Field(alias="boundingBox")
    lines_count: int = Field(alias="linesCount")
    line_height: float = Field(alias="lineheight")
    context: str
    linespace: Optional[float] = Field(None, alias="linespace")
    tran_content: str = Field(alias="tranContent")
    lines: Optional[List[OCRTranslateLine]] = None
    color: Optional[str] = None

    class Config:
        populate_by_name = True


class OCRTranslateResponse(BaseModel):
    """有道OCR翻译API的响应类型"""

    orientation: str
    lan_from: str = Field(alias="lanFrom")
    text_angle: str = Field(alias="textAngle")
    error_code: str = Field(alias="errorCode")
    lan_to: str = Field(alias="lanTo")
    res_regions: List[OCRTranslateRegion] = Field(alias="resRegions")
    render_image: Optional[str] = None

    class Config:
        populate_by_name = True


class TTSResponse(BaseModel):
    """有道 TTS API 的响应类型"""

    error_code: str = Field(alias="errorCode")
    tts_url: Optional[str] = Field(None, alias="ttsUrl")
    message: Optional[str] = None

    class Config:
        populate_by_name = True
