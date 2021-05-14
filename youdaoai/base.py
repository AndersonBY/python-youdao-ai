# -*- coding: utf-8 -*-
# @Author: ander
# @Date:   2021-05-14 12:23:37
# @Last Modified by:   ander
# @Last Modified time: 2021-05-14 13:27:18
import uuid
import requests
import hashlib


YOUDAO_URL = 'https://openapi.youdao.com/'


class Base:

    def __init__(
        self,
        app_key,
        app_secret
    ):
        self.app_key = app_key
        self.app_secret = app_secret

    def _encrypt(self, signStr, method='sha256'):
        if method == 'sha256':
            hash_algorithm = hashlib.sha256()
        elif method == 'md5':
            hash_algorithm = hashlib.md5()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def _truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def _get_salt(self):
        return str(uuid.uuid1())

    def _get_sign(self, q, salt, curtime='', truncate=True, method='sha256'):
        if truncate:
            signStr = self.app_key + self._truncate(q) + salt + curtime + self.app_secret
        else:
            signStr = self.app_key + q + salt + curtime + self.app_secret
        return self._encrypt(signStr, method)

    def _do_request(self, api_path, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(YOUDAO_URL + api_path, data=data, headers=headers)
