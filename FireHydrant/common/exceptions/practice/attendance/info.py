from common.exceptions.base import FireHydrantExceptBase


class PracticeAttendanceInfoExcept(FireHydrantExceptBase):
    MAJOR_HTTP_CODE = 570

    @classmethod
    def attendance_is_not_exists(cls):
        return cls("考勤记录不存在")

    @classmethod
    def attendance_create_fail(cls):
        return cls("排课创建失败")



