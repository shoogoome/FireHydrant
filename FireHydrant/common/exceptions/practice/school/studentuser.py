from common.exceptions.base import FireHydrantExceptBase

class PracticeStudentUserInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 570

    @classmethod
    def studentuser_is_not_exists(cls):
        return cls("学生不存在")

    @classmethod
    def code_or_account_is_exists(cls):
        return cls("该学号或账号已绑定")

    @classmethod
    def create_studentuser_fail(cls):
        return cls("创建学生失败")

