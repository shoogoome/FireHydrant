# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.constants.params import TASK_PUBLIC_WAIT_TIME
from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.enum.task.type import TaskTypeEnum
from common.exceptions.task.classification import TaskClassificationExcept
from common.exceptions.task.task import TaskInfoExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ..logics.task import TaskLogic
from ..models import Task, TaskClassification, TaskApply
from server.resources.logic.info import ResourceLogic
from common.exceptions.task.report import TaskReportExcept
from ..models import TaskReport
from ..logics.report import TaskReportLogic
from common.enum.task.stage import TaskStageEnum

class TaskReportView(FireHydrantView):

    @check_login
    def get(self, request, tid, rid):
        """
        获取任务汇报信息
        :param request:
        :param tid:
        :param rid:
        :return:
        """
        logic = TaskReportLogic(self.auth, tid, rid)
        return SuccessResult(logic.get_report_info())

    @check_login
    def post(self, request, tid):
        """
        提交任务汇报
        :param request:
        :param tid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = TaskLogic(self.auth, tid)

        if logic.task.leader != self.auth.get_account():
            raise TaskReportExcept.no_permission()
        # 每个任务有且仅有一个任务汇报
        if TaskReport.objects.filter(task=logic.task).exists():
            raise TaskReportExcept.report_is_exists()

        with transaction.atomic():
            report = TaskReport.objects.create(
                task=logic.task,
                summary=params.str('summary', desc='总结'),
            )

        # 关联资源元数据
        if params.has('resources'):
            meta_list = {ResourceLogic.decode_token(token) for token in params.list('resources', desc='资源信息')}
            try:
                meta_list.remove(None)
            except:
                pass
            report.resource.set(list(meta_list))
        # 修改任务阶段至结算期
        logic.task.stage = int(TaskStageEnum.SETTLEMENT)

        report.save()
        return SuccessResult(id=report.id)

    @check_login
    def put(self, request, tid, rid):
        """
        修改任务汇报
        :param request:
        :param tid:
        :param rid:
        :return:
        """
        logic = TaskReportLogic(self.auth, tid, rid)
        params = ParamsParser(request.JSON)

        report = logic.report
        with params.diff(report):
            report.summary = params.str('summary', desc='总结')
        # 关联资源元数据
        if params.has('resources'):
            meta_list = {ResourceLogic.decode_token(token) for token in params.list('resources', desc='资源信息')}
            try:
                meta_list.remove(None)
            except:
                pass
            report.resource.set(list(meta_list))

        report.save()
        return SuccessResult(id=rid)

    @check_login
    def delete(self, request, tid, rid):
        """
        删除任务汇报
        :param request:
        :param tid:
        :param rid:
        :return:
        """
        logic = TaskReportLogic(self.auth, tid, rid)

        logic.report.delete()
        return SuccessResult(id=rid)

