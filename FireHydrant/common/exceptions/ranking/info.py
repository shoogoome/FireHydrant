
from common.exceptions.base import FireHydrantExceptBase

class RankingInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 555.1

    @classmethod
    def task_type_error(cls):
        return cls("任务类型参数错误")