# -*- coding: utf-8 -*-
# coding: utf-8

from common.core.http.firehydrant import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ..logics.info import RankingLogic

class RankingTaskView(FireHydrantView):

    def get(self, request):
        """
        任务排行榜
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)
        ranking_type = params.int('ranking_type', desc='榜单类型', require=False, default=0)
        task_type = params.int('task_type', desc='任务类型', require=False, default=0)

        return SuccessResult(RankingLogic.get_task_ranking(task_type=task_type, ranking_type=ranking_type))
