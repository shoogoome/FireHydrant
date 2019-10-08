from common.exceptions.base import FireHydrantExceptBase


class PracticeClassroomInfoExcept(FireHydrantExceptBase):
    MAJOR_HTTP_CODE = 570

    @classmethod
    def classroom_is_not_exists(cls):
        return cls("教室不存在")



