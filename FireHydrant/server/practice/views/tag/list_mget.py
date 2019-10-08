# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logics.school import SchoolLogic
from ...models import PracticeSchool

class PracticeTagListMgetView(FireHydrantView):


    def post(self, request):
        """
        批量获取tag
        :param request:
        :return:
        """
        ...

    def get(self, request):
        """
        获取tag列表
        :param request:
        :return:
        """
        ...