from common.exceptions.base import FireHydrantExceptBase

class PracticeSchoolInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 570

    @classmethod
    def school_is_not_exists(cls):
        return cls("学校不存在")

    @classmethod
    def school_name_is_exists(cls):
        return cls("学校名称已存在")



