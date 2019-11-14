
from common.exceptions.base import FireHydrantExceptBase

class FaceURecordInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 580

    @classmethod
    def record_is_not_exists(cls):
        return cls("记录不存在")
