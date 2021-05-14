# -*- coding: utf-8 -*-
# @Author: anderson
# @Date:   2021-05-13 17:53:01
# @Last Modified by:   ander
# @Last Modified time: 2021-05-14 13:57:34
import wave
import base64
from pathlib import Path
from .base import Base


class SpeechTranslation(Base):

    def _get_base64(self, q):
        audio_file_path = Path(q)
        extension = audio_file_path.suffix.lower()
        if extension != '.wav':
            raise TypeError('不支持的音频类型')

        with open(audio_file_path, 'rb') as file_wav:
            return base64.b64encode(file_wav.read()).decode('utf-8')

    def _get_audio_info(self, audio_file_path):
        with wave.open(audio_file_path, 'rb') as wav_info:
            sample_rate = wav_info.getframerate()
            nchannels = wav_info.getnchannels()

        return {
            'sample_rate': sample_rate,
            'nchannels': nchannels
        }

    def translate(
        self,
        q,
        from_,
        to_,
        rate='auto',
        format_='wav',
        channel='1',
        type_='1',
        ext='mp3',
        voice='0',
        signType='v1',
        version='v1'
    ):
        data = {}
        data['q'] = self._get_base64(q)
        data['from'] = from_
        data['to'] = to_
        data['rate'] = rate if rate != 'auto' else self._get_audio_info(q)['sample_rate']
        data['format'] = format_
        data['channel'] = channel
        data['type'] = type_
        data['ext'] = ext
        data['voice'] = voice
        data['signType'] = signType
        data['version'] = version
        data['salt'] = self._get_salt()
        data['appKey'] = self.app_key
        data['sign'] = self._get_sign(data['q'], data['salt'], truncate=False, method='md5')

        response = self._do_request('speechtransapi', data)
        return response.json()
