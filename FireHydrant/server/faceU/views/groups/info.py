# -*- coding: utf-8 -*-
# coding: utf-8


from common.core.auth.check_login import check_login
from common.core.http.facec import FireHydrantFacecView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.faceU.models import FaceUGroups
from ...logic.groups import FaceUGroupsLogic
from ...logic.safe_delete import delete_group

class FaceUGroupInfo(FireHydrantFacecView):

    @check_login
    def get(self, request, gid):
        """
        获取分组信息
        :param request:
        :param gid:
        :return:
        """
        logic = FaceUGroupsLogic(self.auth, gid)
        return SuccessResult(logic.get_group_info())

    @check_login
    def post(self, request):
        """
        创建分组
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        group = FaceUGroups.objects.create(
            author=self.auth.get_account(),
            title=params.str('title', desc='标题'),
            description=params.str('description', desc='描述', require=False, default='')
        )
        return SuccessResult(id=group.id)

    @check_login
    def put(self, request, gid):
        """
        修改分组信息
        :param request:
        :param gid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = FaceUGroupsLogic(self.auth, gid)

        group = logic.group
        with params.diff(group):
            group.title = params.str('title', desc='标题')
            group.description = params.str('description', desc='描述')

        group.save()
        return SuccessResult(id=gid)

    @check_login
    def delete(self, request, gid):
        """
        删除分组
        :param request:
        :param gid:
        :return:
        """
        logic = FaceUGroupsLogic(self.auth, gid)
        delete_group(logic.group)
        return SuccessResult(id=gid)
