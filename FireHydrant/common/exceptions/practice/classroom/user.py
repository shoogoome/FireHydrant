from common.exceptions.base import FireHydrantExceptBase


class PracticeClassroomUserExcept(FireHydrantExceptBase):
    MAJOR_HTTP_CODE = 570

    @classmethod
    def classroomuser_create_fail(cls):
        return cls("教室使用创建失败")

    @classmethod
    def classroomuser_is_not_exists(cls):
        return cls("教室使用不存在")



