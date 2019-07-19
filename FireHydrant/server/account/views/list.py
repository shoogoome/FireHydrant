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
from ..logics.info import AccountLogic


class AccountListView(FireHydrantView):

    def get(self, request):
        """
        获取用户列表
        :param request:
        :return:
        """
        ...

