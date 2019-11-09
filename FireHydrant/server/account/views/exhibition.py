# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.enum.account.role import AccountRoleEnum
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.account.models import AccountExhibition
from server.resources.logic.info import ResourceLogic
from server.resources.models import ResourcesMeta
from ..logics.exhibition import ExhibitionLogic


class AccountExhibitionView(FireHydrantView):

    @check_login
    def post(self, request, aid):
        """
        创建个人作品展示
        :param request:
        :param aid:
        :return:
        """
        params = ParamsParser(request.JSON)

        with transaction.atomic():
            exhibition = AccountExhibition.objects.create(
                account=self.auth.get_account(),
                title=params.str('title', desc='标题'),
                content=params.str('content', desc='正文'),
                show=params.bool('show', desc='是否展示', default=True, require=False)
            )
        # 关联资源元数据
        if params.has('resources'):
            meta_list = {ResourceLogic.decode_token(token) for token in params.list('resources', desc='资源信息')}
            try:
                meta_list.remove(None)
            except:
                pass
            exhibition.resource.set(list(meta_list))
            exhibition.save()
        return SuccessResult(id=exhibition.id)

    @check_login
    def get(self, request, aid, eid):
        """
        查看用户作品展示详情
        :param request:
        :param aid:
        :param eid:
        :return:
        """
        logic = ExhibitionLogic(self.auth, eid)

        return SuccessResult(logic.get_exhibition_info())

    @check_login
    def put(self, request, aid, eid):
        """
        修改用户作品信息
        :param request:
        :param aid:
        :param eid:
        :return:
        """
        params = ParamsParser(request.JSON)

        logic = ExhibitionLogic(self.auth, eid)
        exhibition = logic.exhibition

        with params.diff(exhibition):
            exhibition.title = params.str('title', desc='标题')
            exhibition.content = params.str('content', desc='正文')
            exhibition.show = params.bool('show', desc='是否展示')

        # 关联资源元数据
        if params.has('resources'):
            meta_list = {ResourceLogic.decode_token(token) for token in params.list('resources', desc='资源信息')}
            try:
                meta_list.remove(None)
            except:
                pass
            exhibition.resource.set(list(meta_list))
            exhibition.save()

        return SuccessResult(id=eid)

    @check_login
    def delete(self, request, aid, eid):
        """
        删除作品
        :param request:
        :param aid:
        :param eid:
        :return:
        """
        logic = ExhibitionLogic(self.auth, eid)

        logic.exhibition.delete()
        return SuccessResult(id=eid)

class AccountExhibitionListView(FireHydrantView):

    @check_login
    def get(self, request, aid):
        """
        获取用户作品列表
        :param request:
        :param aid:
        :return:
        """
        exhibitions = AccountExhibition.objects.filter(
            account_id=aid
        ).values('id', 'create_time', 'update_time', 'title')
        # 对于普通角色他人用户屏蔽不展示的作品
        if self.auth.get_account().role != int(AccountRoleEnum.ADMIN) and \
                aid != self.auth.get_account().id:
            exhibitions = exhibitions.filter(show=True)

        return SuccessResult(list(exhibitions) if exhibitions.exists() else list())
