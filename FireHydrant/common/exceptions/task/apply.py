
from common.exceptions.base import FireHydrantExceptBase

class TaskInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 553.3

    @classmethod
    def apply_is_not_exists(cls):
        return cls("申请表不存在")




