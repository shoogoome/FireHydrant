
from common.exceptions.base import FireHydrantExceptBase

class ResourceInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 554.2

    @classmethod
    def meta_is_not_exists(cls):
        return cls("资源元数据不存在")



