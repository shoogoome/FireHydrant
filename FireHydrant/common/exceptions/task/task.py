
from common.exceptions.base import FireHydrantExceptBase

class TaskInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 553.2

    @classmethod
    def task_is_not_exists(cls):
        return cls("任务不存在")

    @classmethod
    def task_type_is_not_exists(cls):
        return cls("分类不存在")

    @classmethod
    def is_not_in_release(cls):
        return cls("任务不在发布期不允许修改基础信息")


