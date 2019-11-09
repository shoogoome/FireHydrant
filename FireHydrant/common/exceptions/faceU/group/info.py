
from common.exceptions.base import FireHydrantExceptBase

class FaceUGroupInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 580

    @classmethod
    def group_is_not_exists(cls):
        return cls("分组不存在")
