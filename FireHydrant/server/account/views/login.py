#-*- coding: utf-8 -*-
# coding: utf-8

from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.utils.helper.params import ParamsParser
from ..models import Account
from django.db import transaction
from common.exceptions.account.info import AccountInfoExcept
from common.utils.helper.result import SuccessResult
from common.utils.helper.m_t_d import model_to_dict
from ..logics.info import AccountLogic
from common.constants.length_limitation import *
from common.utils.hash import signatures


class AccountLoginView(FireHydrantView):

    def post(self, request):
        """
        登录
        :param request:
        :return:
        """
        # TODO: 后续加上人机验证
        params = ParamsParser(request.JSON)
        password = params.str('password', desc='密码', min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)
        username = params.str('username', desc='用户名', max_length=MAX_USERNAME_LENGTH)

        accounts = Account.objects.filter_cache(username=username)
        # 因为得到的是list类型所以直接使用len即可，不会造成多次数据库io操作
        if len(accounts) == 0 or not signatures.compare_password(password, accounts[0].password):
            raise AccountInfoExcept.login_error()

        self.auth.set_account(accounts[0])
        self.auth.set_session()
        return SuccessResult(id=accounts[0].id)

    def get(self, request):
        """
        检查是否登录
        :param request:
        :return:
        """
        if self.auth.is_login():
            return SuccessResult(id=self.auth.get_account().id)
        return SuccessResult(id=None)


class AccountLogoutView(FireHydrantView):

    def post(self, request):
        """
        登出
        :param request:
        :return:
        """
        status = 'OK'

        self.auth.set_account(None)
        self.auth.set_session()

        return SuccessResult(status=status)







    
