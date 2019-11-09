
from common.exceptions.base import FireHydrantExceptBase

class FaceUGroupManageExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 580

    @classmethod
    def insert_fail(cls):
        return cls("创建数据失败")

    @classmethod
    def member_is_not_exists(cls):
        return cls("成员不存在")
