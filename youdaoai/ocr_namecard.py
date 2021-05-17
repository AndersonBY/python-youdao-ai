# -*- coding: utf-8 -*-
# @Author: anderson
# @Date:   2021-05-13 17:53:01
# @Last Modified by:   ander
# @Last Modified time: 2021-05-17 14:03:17
import time
import base64
from pathlib import Path
from .base import Base


class OCRNamecard(Base):

    def _get_base64(self, q):
        p = Path(q)
        if p.exists():
            with open(q, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        else:
            return q

    def recognize(
        self,
        img,
        structureType='namecard',
        docType='json'
    ):
        data = {}
        data['q'] = self._get_base64(img)
        data['structureType'] = structureType
        data['docType'] = docType
        data['signType'] = 'v3'
        data['curtime'] = str(int(time.time()))
        data['salt'] = self._get_salt()
        data['appKey'] = self.app_key
        data['sign'] = self._get_sign(data['q'], data['salt'], data['curtime'])

        response = self._do_request('ocr_structure', data)
        return response.json()
