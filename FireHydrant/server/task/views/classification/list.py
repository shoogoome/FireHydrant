# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.constants.length_limitation import *
from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.enum.team.role import TeamRoleEnum
from common.exceptions.team.info import TeamInfoExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult



class TaskClassificationListView(FireHydrantView):

    def get(self, request):
        """
        获取任务分类列表
        :param request:
        :return:
        """
        ...