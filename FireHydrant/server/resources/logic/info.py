from ..models import ResourcesMeta
from common.exceptions.resources.info import ResourceInfoExcept
from .client import LiumaClient

class ResourceLogic(object):

    def __init__(self, auth, mid):
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

    def get_download_token(self):
        """
        获取下载token
        :return:
        """
        return self.client.get_download_token(self.meta.hash)

    def get_upload_token(self):
        """
        获取上传token
        :return:
        """
        return self.client.get_upload_token(self.meta.hash)

