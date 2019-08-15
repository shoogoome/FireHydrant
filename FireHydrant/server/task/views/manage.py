# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.constants.params import TASK_PUBLIC_WAIT_TIME
from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.enum.task.type import TaskTypeEnum
from common.exceptions.task.classification import TaskClassificationExcept
from common.exceptions.task.task import TaskInfoExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ..logics.task import TaskLogic
from ..models import Task, TaskClassification, TaskApply
from common.enum.task.stage import TaskStageEnum
from server.account.models import AccountExhibition


class TaskManageView(FireHydrantView):

    @check_login
    def get(self, request, tid):
        """
        获取任务申请列表
        :param request:
        :param tid:
        :return:
        """
        ...

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
            ex_ids = params.list('exhibition')
            if not set(ex_ids).issubset(exhibitions):
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



