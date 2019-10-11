from common.exceptions.base import FireHydrantExceptBase


class PracticeEvaluateExcept(FireHydrantExceptBase):
    MAJOR_HTTP_CODE = 570

    @classmethod
    def evaluate_is_not_exists(cls):
        return cls("评价不存在")

    @classmethod
    def evaluate_create_fail(cls):
        return cls("评价创建失败")



