# -*- coding: utf-8 -*-
# @Author: anderson
# @Date:   2021-05-13 17:53:01
# @Last Modified by:   ander
# @Last Modified time: 2021-05-17 13:59:03
import time
import base64
from pathlib import Path
from .base import Base


class OCRTable(Base):

    def _get_base64(self, q):
        p = Path(q)
        if p.exists():
            with open(q, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        else:
            return q

    def _save_file(self, excel_filepath, base64_data):
        with open(excel_filepath, 'wb') as fo:
            fo.write(base64.b64decode(base64_data.encode('utf-8')))

    def recognize(
        self,
        img,
        docType,
        excel_filepath=None,
        angle=None
    ):
        data = {}
        data['q'] = self._get_base64(img)
        data['type'] = '1'
        data['docType'] = docType
        data['signType'] = 'v3'
        data['curtime'] = str(int(time.time()))
        data['salt'] = self._get_salt()
        data['appKey'] = self.app_key
        data['sign'] = self._get_sign(data['q'], data['salt'], data['curtime'])

        if angle:
            data['angle'] = angle

        response = self._do_request('ocr_table', data)
        result = response.json()
        if docType.lower() == 'excel' and result['errorCode'] == '0' and excel_filepath is not None:
            self._save_file(excel_filepath, result['Result']['tables'][0])
        return result
