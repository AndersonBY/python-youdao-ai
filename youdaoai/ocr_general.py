# -*- coding: utf-8 -*-
# @Author: anderson
# @Date:   2021-05-13 17:53:01
# @Last Modified by:   ander
# @Last Modified time: 2021-05-17 12:09:12
import time
import base64
from pathlib import Path
from .base import Base


class OCRGeneral(Base):

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
        langType='auto',
        detectType='10012',
        imageType='1',
        angle=None,
        column=None,
        rotate=None,
    ):
        data = {}
        data['img'] = self._get_base64(img)
        data['langType'] = langType
        data['detectType'] = detectType
        data['imageType'] = imageType
        data['signType'] = 'v3'
        data['curtime'] = str(int(time.time()))
        data['salt'] = self._get_salt()
        data['appKey'] = self.app_key
        data['sign'] = self._get_sign(data['img'], data['salt'], data['curtime'])

        if angle:
            data['angle'] = angle
        if column:
            data['column'] = column
        if rotate:
            data['rotate'] = rotate

        response = self._do_request('ocrapi', data)
        return response.json()
