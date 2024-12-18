# -*- coding: utf-8 -*-
# @Author: anderson
# @Date:   2021-05-13 17:53:01
# @Last Modified by:   ander
# @Last Modified time: 2021-05-14 13:58:30
import time
import os
from .base import Base


class Translation(Base):

    def translate(
        self,
        q,
        from_,
        to_,
        ext=None,
        audio_path=None,
        voice=None,
        strict=None,
        vocabId=None,
    ):
        data = {}
        data['q'] = q
        data['from'] = from_
        data['to'] = to_
        data['signType'] = 'v3'
        data['curtime'] = str(int(time.time()))
        data['salt'] = self._get_salt()
        data['appKey'] = self.app_key
        data['sign'] = self._get_sign(q, data['salt'], data['curtime'])

        if ext:
            data['ext'] = ext
        if not audio_path:
            audio_path = os.path.join(os.getcwd(), str(int(round(time.time() * 1000))) + ".mp3")
        if voice:
            data['voice'] = voice
        if strict:
            data['strict'] = strict
        if vocabId:
            data['vocabId'] = vocabId

        response = self._do_request('api', data)
        contentType = response.headers['Content-Type']
        if contentType == "audio/mp3":
            with open(audio_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            return response.json()
