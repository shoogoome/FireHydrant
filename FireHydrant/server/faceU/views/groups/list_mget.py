# -*- coding: utf-8 -*-
# coding: utf-8


from common.core.auth.check_login import check_login
from common.core.http.facec import FireHydrantFacecView
from common.enum.account.role import AccountRoleEnum
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.faceU.models import FaceUGroups
from ...logic.groups import FaceUGroupsLogic


class FaceUGroupListMget(FireHydrantFacecView):

    @check_login
    def get(self, request):
        """
        获取分组列表
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        groups = FaceUGroups.objects.values('id', 'update_time', 'nickname')
        if params.has('account') and self.auth.get_account().role == int(AccountRoleEnum.ADMIN):
            groups = groups.filter(author_id=params.int('account', desc='用户id'))
        else:
            groups = groups.filter(author=self.auth.get_account())

        if params.has('title'):
            groups = groups.filter(groups__contains=params.str('groups', desc='标题'))

        groups_list, pagination = slicer(groups, limit=limit, page=page)()()
        return SuccessResult(accounts=groups_list, pagination=pagination)

    @check_login
    def post(self, request):
        """
        批量获取分组信息
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = FaceUGroupsLogic(self.auth)
        ids = params.list('ids', desc='分组id列表')
        _auth_id = self.auth.get_account().id
        _admin = self.auth.get_account().role == int(AccountRoleEnum.ADMIN)

        data = []
        groups = FaceUGroups.objects.get_many(ids)
        for group in groups:
            try:
                logic.group = group
                if logic.group.author_id != _auth_id or not _admin:
                    continue
                data.append(logic.get_group_info())
            except:
                pass

        return SuccessResult(data)
