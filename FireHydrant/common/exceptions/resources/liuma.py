
from common.exceptions.base import FireHydrantExceptBase

class LiumaInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 554.1

    @classmethod
    def get_token_fail(cls):
        return cls("获取令牌失败")



