#-*- coding: utf-8 -*-
# coding: utf-8

from django.db.models import Q

from common.constants.length_limitation import *
from common.core.http.view import FireHydrantView
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ..models import Account


class AccountListView(FireHydrantView):

    def get(self, request):
        """
        获取用户列表
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        accounts = Account.objects.values('id', 'update_time', 'username', 'nickname')
        if params.has('role'):
            accounts = accounts.filter(role=params.int('role', desc='角色'))
        if params.has('key'):
            key = params.str('key', desc='关键字 过滤用户名和昵称', max_length=MAX_USERNAME_LENGTH)
            accounts = accounts.filter(
                Q(username__contains=key) |
                Q(nickname__contains=key)
            )

        account_list, pagination = slicer(accounts, limit=limit, page=page)()()

        return SuccessResult(accounts=account_list, pagination=pagination)