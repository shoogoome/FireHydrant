from ..models import ResourcesMeta
from common.exceptions.resources.info import ResourceInfoExcept
from common.utils.hash.signatures import cookie_signature
from .client import LiumaClient
import time
import json
import base64

class ResourceLogic(object):

    def __init__(self, auth, mid=''):
        """
        INIT
        :param auth:
        :param mid:
        """
        self.auth = auth
        self.client = LiumaClient()

        if isinstance(mid, ResourcesMeta):
            self.meta = mid
        else:
            self.meta = self.get_meta_model(mid)

    def get_meta_model(self, mid):
        """
        获取资源元数据信息
        :param mid:
        :return:
        """
        if mid is None or mid == '':
            return

        meta = ResourcesMeta.objects.get_once(pk=mid)
        if meta is None:
            raise ResourceInfoExcept.meta_is_not_exists()

        return meta

    @staticmethod
    def get_download_token(hash):
        """
        获取下载token
        :return:
        """
        client = LiumaClient()
        return client.get_download_token(hash)

    @staticmethod
    def get_upload_token(hash):
        """
        获取上传token
        :param hash:
        :return:
        """
        client = LiumaClient()
        return client.get_upload_token(hash)

    def upload_finish(self, token, name, expire=3600):
        """
        完成上传并生成token token过期时间一小时
        :param token:
        :param name:
        :param expire:
        :return:
        """
        if self.meta is None:
            return False, ""

        ok = self.client.upload_finish(token, name)
        # 成功上传则创建token
        if ok:
            payload = {
                "expire_at": int(time.time() + expire),
                "meta": self.meta.id
            }
            payload_str = json.dumps(payload)
            token = cookie_signature(payload_str)
            payload_encode = base64.b64encode(payload_str.encode("utf-8")).decode()

            return True, '{}.{}'.format(payload_encode, token)
        # 否则删除当前元数据记录
        # else:
        #     self.meta.delete()
        return False, ""

    @staticmethod
    def decode_token(token):
        """
        解码token
        :param token:
        :return:
        """
        if not token or not isinstance(token, str):
            return None
        token_list = token.split('.')
        # 格式错误
        if len(token_list) != 2:
            return None

        payload_str = base64.b64decode(token_list[0]).decode()
        # 签名验证
        if cookie_signature(payload_str) != token_list[1]:
            return None

        payload = json.loads(payload_str)
        if int(time.time()) >= payload.get('expire_at', -1):
            return None
        meta_id = payload.get('meta', -1)
        return meta_id
