# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult


class PracticeArrangementStudentInfoView(FireHydrantView):


    def post(self, request, sid, cid, aid):
        """
        批量导入学生信息
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        ...

    def delete(self, request, sid, cid, aid):
        """
        批量移除学生
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        ...