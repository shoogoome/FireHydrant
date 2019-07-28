
from common.exceptions.base import FireHydrantExceptBase

class TaskClassificationExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 553.1

    @classmethod
    def classification_is_not_exists(cls):
        return cls("分类不存在")
