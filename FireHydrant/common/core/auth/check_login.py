from django.http import JsonResponse
from common.constants.params import *
from common.exceptions.account.info import AccountInfoExcept


def check_login(func):
    """
    登陆检查装饰器
    :param func:
    :return:
    """
    def check(*args, **kwargs):
        self = args[0]
        if self.auth.is_login():
            return func(*args, **kwargs)
        raise AccountInfoExcept.is_not_login()

    return check