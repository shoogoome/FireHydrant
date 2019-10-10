from common.exceptions.base import FireHydrantExceptBase

class PracticeTagInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 570

    @classmethod
    def tag_is_not_exists(cls):
        return cls("标签不存在")

    @classmethod
    def tag_create_fail(cls):
        return cls("创建标签失败")

    @classmethod
    def tag_name_is_exists(cls):
        return cls("标签已存在")

    @classmethod
    def parent_is_not_exists(cls):
        return cls("父标签不存在")

    @classmethod
    def parent_appoint_illegal(cls):
        return cls("父标签设置非法")



