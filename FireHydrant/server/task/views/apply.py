# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.enum.account.role import AccountRoleEnum
from common.enum.task.stage import TaskStageEnum
from common.exceptions.task.task import TaskInfoExcept
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.account.models import AccountExhibition
from ..logics.apply import TaskApplyLogic
from ..logics.task import TaskLogic
from ..models import TaskApply


class TaskApplyInfoView(FireHydrantView):

    @check_login
    def get(self, request, tid, aid):
        """
        获取任务申请表信息
        :param request:
        :param tid:
        :param aid:
        :return:
        """
        logic = TaskApplyLogic(self.auth, aid)

        return SuccessResult(logic.get_apply_info())

    @check_login
    def post(self, request, tid):
        """
        提交任务申请
        :param request:
        :param tid:
        :return:
        """
        logic = TaskLogic(self.auth, tid)
        params = ParamsParser(request.JSON)

        if logic.task.stage != int(TaskStageEnum.RELEASE):
            raise TaskInfoExcept.no_permission()

        if params.has('exhibition'):
            # 成就选择异常 （一般是恶意请求，所以直接报无权限）
            exhibitions = AccountExhibition.objects.filter(account=self.auth.get_account()).values('id')
            ex_ids = params.list('exhibition', desc='成就id列表')
            if not set(ex_ids).issubset([i['id'] for i in exhibitions]):
                raise TaskInfoExcept.no_permission()

        with transaction.atomic():
            apply = TaskApply.objects.create(
                task=logic.task,
                author=self.auth.get_account(),
                content=params.str('content', desc='正文'),
            )
        if params.has('exhibition'):
            apply.exhibition.set(ex_ids)
            apply.save()

        return SuccessResult(id=apply.id)

    @check_login
    def put(self, request, tid, aid):
        """
        修改任务申请表内容
        :param request:
        :param tid:
        :return:
        """
        logic = TaskApplyLogic(self.auth, aid)
        params = ParamsParser(request.JSON)

        apply = logic.apply

        if params.has('exhibition'):
            # 成就选择异常 （一般是恶意请求，所以直接报无权限）
            exhibitions = AccountExhibition.objects.filter(account=self.auth.get_account()).values('id')
            ex_ids = params.list('exhibition')
            if not set(ex_ids).issubset([i["id"] for i in exhibitions]):
                raise TaskInfoExcept.no_permission()
            apply.exhibition.set(ex_ids)

        with params.diff(apply):
            apply.content = params.str('content', desc='正文')
        apply.save()

        return SuccessResult(id=aid)

    @check_login
    def delete(self, request, tid, aid):
        """
        删除任务申请表
        :param request:
        :param tid:
        :param aid:
        :return:
        """
        logic = TaskApplyLogic(self.auth, aid)
        if logic.apply.author != self.auth.get_account() and \
                self.auth.get_account().role != int(AccountRoleEnum.ADMIN):
            raise TaskInfoExcept.no_permission()
        logic.apply.delete()
        return SuccessResult(id=aid)

class TaskApplyListView(FireHydrantView):

    @check_login
    def get(self, request, tid):
        """
        获取任务申请列表
        :param request:
        :param tid:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)
        logic = TaskLogic(self.auth, tid)

        if logic.task.author != self.auth.get_account() and \
                self.auth.get_account().role != int(AccountRoleEnum.ADMIN):
            raise TaskInfoExcept.no_permission()

        applies = TaskApply.objects.filter(task=logic.task).values(
            'id', 'create_time', 'update_time', 'author', 'author__nickname'
        )

        @slicer(applies, limit=limit, page=page)
        def get_apply_list(obj):
            obj['author'] = {
                'id': obj['author'],
                'nickname': obj['author__nickname']
            }
            del obj['author__nickname']
            return obj
        apply_list, pagination = get_apply_list()
        return SuccessResult(applies=apply_list, pagination=pagination)
