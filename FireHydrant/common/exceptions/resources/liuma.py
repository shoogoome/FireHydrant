
from common.exceptions.base import FireHydrantExceptBase

class LiumaInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 554.1

    @classmethod
    def get_download_token_fail(cls):
        return cls("获取下载令牌失败")



