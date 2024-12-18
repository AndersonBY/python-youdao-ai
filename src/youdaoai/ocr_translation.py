# -*- coding: utf-8 -*-
# @Author: anderson
# @Date:   2021-05-13 17:53:01
# @Last Modified by:   ander
# @Last Modified time: 2021-05-14 13:46:48
import time
import os
import base64
from pathlib import Path
from .base import Base


class OCRTranslation(Base):

    def _get_base64(self, q):
        p = Path(q)
        if p.exists():
            with open(q, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        else:
            return q

    def translate(
        self,
        q,
        from_,
        to_,
        ext=None,
        audio_path=None,
        docType=None,
        render=None,
        nullIsError=None,
    ):
        data = {}
        data['q'] = self._get_base64(q)
        data['from'] = from_
        data['to'] = to_
        data['type'] = '1'
        data['salt'] = self._get_salt()
        data['appKey'] = self.app_key
        data['sign'] = self._get_sign(data['q'], data['salt'], truncate=False, method='md5')

        if ext:
            data['ext'] = ext
        if not audio_path:
            audio_path = os.path.join(os.getcwd(), str(int(round(time.time() * 1000))) + ".mp3")
        if docType:
            data['docType'] = docType
        if render:
            data['render'] = render
        if nullIsError:
            data['nullIsError'] = nullIsError

        response = self._do_request('ocrtransapi', data)
        contentType = response.headers['Content-Type']
        if contentType == "audio/mp3":
            with open(audio_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            return response.json()
