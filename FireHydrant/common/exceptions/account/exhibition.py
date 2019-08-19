
from common.exceptions.base import FireHydrantExceptBase

class AccountExhibitionExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 551.2

    @classmethod
    def exhibition_is_not_exists(cls):
        return cls("作品展示信息不存在")