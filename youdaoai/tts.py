# -*- coding: utf-8 -*-
# @Author: anderson
# @Date:   2021-05-13 17:53:01
# @Last Modified by:   ander
# @Last Modified time: 2021-05-24 13:08:30
from .base import Base


class TTS(Base):

    def build(
        self,
        q,
        langType,
        filepath,
        voice=0,
        speed=1,
        volumn=1.0
    ):
        data = {}
        data['q'] = q
        data['langType'] = langType
        data['voice'] = str(voice)
        data['speed'] = str(speed)
        data['volumn'] = str(volumn)
        data['salt'] = self._get_salt()
        data['appKey'] = self.app_key
        data['sign'] = self._get_sign(data['q'], data['salt'], truncate=False, method='md5')

        response = self._do_request('ttsapi', data)
        if response.headers['Content-Type'] == "audio/mp3":
            with open(filepath, 'wb') as f:
                f.write(response.content)
                return True
        else:
            return response.json()
