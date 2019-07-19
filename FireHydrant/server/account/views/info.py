#-*- coding: utf-8 -*-
# coding: utf-8

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from ..models import Account
from django.db import transaction
from common.exceptions.account.info import AccountInfoExcept
from common.utils.helper.result import SuccessResult
from common.utils.helper.m_t_d import model_to_dict
from common.utils.hash import signatures
from common.decorate.administrators import administrators
from ..logics.info import AccountLogic


class AccountInfoView(FireHydrantView):

    fetch_me = False

    @check_login
    def get(self, request, aid=''):
        """
        获取账户信息
        :param request:
        :param aid:
        :return:
        """
        logic = AccountLogic(self.auth, self.auth.get_account() if self.fetch_me else aid)

        return SuccessResult(logic.get_account_info())

    @check_login
    def post(self, request):
        """
        批量获取账户信息
        :param request:
        :return:
        """
        logic = AccountLogic(self.auth)
        params = ParamsParser(request.JSON)
        account_ids = params.list('ids', desc='用户id列表')

        data = list()
        accounts = Account.objects.get_many(pks=account_ids)
        for account in accounts:
            try:
                logic.account = account
                data.append(logic.get_account_info())
            except:
                pass

        return SuccessResult(data)

    @check_login
    def put(self, request, aid=''):
        """
        修改用户信息
        :param request:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)
        if self.fetch_me:
            logic = AccountLogic(self.auth, self.auth.get_account())
        else:
            # administrators(lambda x: True)(self)
            logic = AccountLogic(self.auth, aid)

        account = logic.account

        with params.diff(account):
            account.nickname = params.str('nickname', desc='昵称')
            account.sex = params.int('sex', desc='性别')
            account.motto = params.str('motto', desc='一句话签名')

        if params.has('new_password'):
            new_password = params.str('new_password', desc='新密码')
            old_password = params.str('old_password', desc='旧密码')
            if not signatures.compare_password(old_password, account.password):
                raise AccountInfoExcept.old_password_error()
            account.password = signatures.build_password_signature(new_password, signatures.gen_salt())
        # 卡权限
        if params.has('role'):
            ...






    def delete(self, request, aid):
        """
        删除账户
        :param request:
        :param aid:
        :return:
        """
        ...









