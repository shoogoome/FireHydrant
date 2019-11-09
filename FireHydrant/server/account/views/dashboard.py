# -*- coding: utf-8 -*-
# coding: utf-8

from common.constants.length_limitation import *
from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.exceptions.account.info import AccountInfoExcept
from common.utils.hash import signatures
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.resources.logic.info import ResourceLogic
from ..logics.info import AccountLogic
from ..models import Account
from server.task.models import Task, TaskApply


class AccountInfoView(FireHydrantView):

    @check_login
    def get(self, request, aid):
        """
        获取仪表盘
        :param request:
        :param aid:
        :return:
        """
        logic = AccountLogic(self.auth, aid)
        # 获取发布任务信息
        tasks = Task.objects.filter(author=logic.account).values(
            'id', 'title', 'stage', 'task_type', 'create_time')
        # 获取接受任务信息
        works = logic.account.task_workers_set.all().values(
            'id', 'title', 'stage', 'task_type', 'create_time')

        data = {
            'tasks': [i for i in tasks],
            'works': [i for i in works]
        }
        # 本人则获取申请任务信息
        if logic.account == self.auth.get_account():
            apply = TaskApply.objects.filter(author=logic.account).values(
                'task__id', 'task__title', 'id', 'create_time',
            )
            data['apply'] = [i for i in apply]
        return SuccessResult(data)





