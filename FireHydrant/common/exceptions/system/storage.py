
from common.exceptions.base import FireHydrantExceptBase

class StorageInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 591.1

    @classmethod
    def model_is_not_exists(cls):
        return cls("存储模块不存在")

    @classmethod
    def decode_fail(cls):
        return cls("解析失败")



