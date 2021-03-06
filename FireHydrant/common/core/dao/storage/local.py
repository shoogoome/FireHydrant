import os
from common.constants.storages import STORAGE_MAPPING
from common.exceptions.system.storage import StorageInfoExcept
from common.utils.hash.signatures import generate_token, cookie_signature
import base64
import time
import json
from common.constants.params import *
import re


class FireHydrantLocalStorage(object):

    def __init__(self, model):
        """
        FIREHYDRANT本地存储
        :param model:
        """
        if model not in STORAGE_MAPPING:
            raise StorageInfoExcept.model_is_not_exists()
        self.model = model
        self._root = STORAGE_MAPPING[model]

    def save_file(self, path, file, open_type='w'):
        """
        保存文件
        :param path:
        :param file:
        :param open_type:
        :return:
        """
        dirname, filename = os.path.split(path)
        os.system('mkdir -p {}'.format(os.path.join(self._root, dirname)))
        with open(os.path.join(self._root, path), open_type) as fp:
            fp.write(file)

        return "storage://{}@{}".format(self.model, path)

    @staticmethod
    def generate_token(path, aid=None, expire=COOKIE_EFFECTIVE_TIME):
        """
        生成下载密钥
        :param aid:
        :param path:
        :param expire:
        :return:
        """
        if not path:
            return ""
        payload = {
            "expire_at": int(time.time() + expire),
            "account_id": aid,
            "path": path,
            "public": False if aid else True
        }
        return generate_token(payload)

    @staticmethod
    def decode_token(token, auth):
        """
        解析下载密钥
        :param token:
        :param auth:
        :return:
        """
        if not token:
            raise StorageInfoExcept.decode_fail()
        user_token = token.split('.')
        # 格式错误
        if len(user_token) != 2:
            raise StorageInfoExcept.decode_fail()

        payload_str = base64.b64decode(user_token[0]).decode()
        # 签名验证
        if cookie_signature(payload_str) != user_token[1]:
            raise StorageInfoExcept.decode_fail()

        payload = json.loads(payload_str)
        # 过期时间验证
        if int(time.time()) >= payload.get('expire_at', -1):
            raise StorageInfoExcept.decode_fail()
        # 私有验证
        if not payload.get("public", False) and \
                (not auth.is_login() or auth.get_account().id != payload.get('account_id', -1)):
            raise StorageInfoExcept.decode_fail()
        # 解析资源路径
        path = payload.get('path', '')
        if not path:
            raise StorageInfoExcept.decode_fail()
        # 格式验证
        r = re.findall('^storage://(.*?)@(.*?)$', path)
        if len(r) != 1:
            raise StorageInfoExcept.decode_fail()

        model, filename = r[0]
        return os.path.split(os.path.join(STORAGE_MAPPING[model], filename))
