
from common.exceptions.base import FireHydrantExceptBase

class TeamInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 552.1

    @classmethod
    def team_is_not_exists(cls):
        return cls("队伍不存在")

    @classmethod
    def nickname_is_exists(cls):
        return cls("队伍名已存在")

    @classmethod
    def leader_is_not_exists(cls):
        return cls("新队长不在当前队伍")

    @classmethod
    def already_in_team(cls):
        return cls("已加入其他队伍")

    @classmethod
    def password_error(cls):
        return cls("密码错误")

    @classmethod
    def team_is_full(cls):
        return cls("队伍已满员")

    @classmethod
    def role_error(cls):
        return cls("角色不存在")
