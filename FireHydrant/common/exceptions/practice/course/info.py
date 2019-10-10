from common.exceptions.base import FireHydrantExceptBase


class PracticeCourseInfoExcept(FireHydrantExceptBase):
    MAJOR_HTTP_CODE = 570

    @classmethod
    def course_is_not_exists(cls):
        return cls("课程不存在")

    @classmethod
    def course_create_fail(cls):
        return cls("课程创建失败")



