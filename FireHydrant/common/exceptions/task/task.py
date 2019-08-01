
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
    def task_conduct(cls):
        return cls("任务进行期间不得修改基础信息")


