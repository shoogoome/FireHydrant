
from common.exceptions.base import FireHydrantExceptBase

class FaceUAccountInfoExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 580

    @classmethod
    def username_is_exists(cls):
        return cls("用户名已存在")

    @classmethod
    def is_not_login(cls):
        return cls("尚未登录")

    @classmethod
    def account_is_not_exists(cls):
        return cls("该用户不存在")

    @classmethod
    def login_error(cls):
        return cls("用户名不存在或密码不正确")

    @classmethod
    def old_password_error(cls):
        return cls("旧密码错误")

    @classmethod
    def no_permission(cls):
        return cls("无该权限")

    @classmethod
    def nickname_is_exists(cls):
        return cls("昵称已存在")

    @classmethod
    def avator_save_fail(cls):
        return cls("头像保存失败")

    @classmethod
    def token_error(cls, errmsg="get token error"):
        return cls(errmsg)
