
from common.exceptions.base import FireHydrantExceptBase

class TeamInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 552.1

    @classmethod
    def already_in_team(cls):
        return cls("已加入队伍不得创建队伍")

    @classmethod
    def team_is_not_exists(cls):
        return cls("队伍不存在")

    @classmethod
    def nickname_is_exists(cls):
        return cls("队伍名已存在")
