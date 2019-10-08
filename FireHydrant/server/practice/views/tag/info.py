# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logics.school import SchoolLogic
from ...models import PracticeSchool

class PracticeTagView(FireHydrantView):


    def post(self, request):
        """
        创建tag
        :param request:
        :return:
        """
        ...

    def get(self, request, tid):
        """
        获取tag信息
        :param request:
        :param tid:
        :return:
        """
        ...

    def put(self, request, tid):
        """
        修改tag信息
        :param request:
        :param tid:
        :return:
        """
        ...

    def delete(self, request, tid):
        """
        删除tag
        :param request:
        :param tid:
        :return:
        """
        ...