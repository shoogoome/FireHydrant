from common.exceptions.base import FireHydrantExceptBase

class TaskReportExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 553.4

    @classmethod
    def report_is_not_exists(cls):
        return cls("任务汇报不存在")

    @classmethod
    def no_permission(cls):
        return cls("无权限执行此操作")

    @classmethod
    def report_is_exists(cls):
        return cls("该任务已提交任务汇报")




