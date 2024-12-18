# -*- coding: utf-8 -*-
# @Author: anderson
# @Date:   2021-05-13 17:53:01
# @Last Modified by:   ander
# @Last Modified time: 2021-05-24 13:54:20
import wave
import time
import base64
from pathlib import Path
from .base import Base


class ASR(Base):

    def _get_base64(self, q):
        audio_file_path = Path(q)
        extension = audio_file_path.suffix.lower()
        if extension not in ('.wav', '.aac', '.mp3'):
            raise TypeError('不支持的音频类型')

        with open(audio_file_path, 'rb') as file_wav:
            return base64.b64encode(file_wav.read()).decode('utf-8')

    def _get_audio_info(self, audio_file_path_str):
        audio_file_path = Path(audio_file_path_str)
        extension = audio_file_path.suffix.lower()
        if extension != '.wav':
            raise TypeError('非.wav格式音频请手动指定采样率')

        with wave.open(audio_file_path_str, 'rb') as wav_info:
            sample_rate = wav_info.getframerate()
            nchannels = wav_info.getnchannels()

        return {
            'sample_rate': sample_rate,
            'nchannels': nchannels
        }

    def recognize(
        self,
        q,
        langType,
        rate='auto',
        format_='wav',
        channel='1',
    ):
        data = {}
        data['q'] = self._get_base64(q)
        data['langType'] = langType
        data['rate'] = str(rate) if rate != 'auto' else self._get_audio_info(q)['sample_rate']
        data['curtime'] = str(int(time.time()))
        data['format'] = str(format_)
        data['channel'] = str(channel)
        data['signType'] = 'v2'
        data['type'] = '1'
        data['salt'] = self._get_salt()
        data['appKey'] = self.app_key
        data['sign'] = self._get_sign(data['q'], data['salt'], data['curtime'])

        response = self._do_request('asrapi', data)
        return response.json()
