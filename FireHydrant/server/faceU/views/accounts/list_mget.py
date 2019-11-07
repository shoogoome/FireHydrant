# -*- coding: utf-8 -*-
# coding: utf-8


from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.faceU.models import FaceUAccount
from ...logic.account import FaceUAccountLogic


class FaceUAccountListMget(FireHydrantView):

    @check_login
    def get(self, request):
        """
        获取用户列表
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        accounts = FaceUAccount.objects.values('id', 'update_time', 'nickname')
        if params.has('nickname'):
            accounts = accounts.filter(nickname__contains=params.str('nickname'))

        account_list, pagination = slicer(accounts, limit=limit, page=page)()()
        return SuccessResult(accounts=account_list, pagination=pagination)

    @check_login
    def post(self, request):
        """
        批量获取用户信息
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = FaceUAccountLogic(self.auth)
        ids = params.list('ids', desc='用户id列表')

        data = []
        accounts = FaceUAccount.objects.get_many(ids)
        for account in accounts:
            try:
                logic.account = account
                data.append(logic.get_account_info())
            except:
                pass

        return SuccessResult(data)
