from common.exceptions.base import FireHydrantExceptBase


class PracticeArrangementInfoExcept(FireHydrantExceptBase):
    MAJOR_HTTP_CODE = 570

    @classmethod
    def arrangement_is_not_exists(cls):
        return cls("排课不存在")

    @classmethod
    def arrangement_create_fail(cls):
        return cls("排课创建失败")



