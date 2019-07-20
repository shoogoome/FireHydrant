
from common.exceptions.base import FireHydrantExceptBase

class TeamInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 552.1

    @classmethod
    def already_in_team(cls):
        return cls("已加入队伍不得创建队伍")
