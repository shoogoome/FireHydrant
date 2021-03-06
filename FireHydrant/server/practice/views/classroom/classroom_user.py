# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.exceptions.practice.classroom.user import PracticeClassroomUserExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logics.classroom import ClassroomLogic
from ...models import PracticeClassroomUser


class PracticeClassroomUserInfoView(FireHydrantView):

    @check_login
    def get(self, request, sid, cid):
        """
        获取教室使用情况
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        logic = ClassroomLogic(self.auth, sid, cid)
        return SuccessResult(logic.get_classroom_user())

    @check_login
    def post(self, request, sid, cid):
        """
        教室安排使用
        :param request:
        :param sid:
        :param cid:
        :return:
        """
        logic = ClassroomLogic(self.auth, sid, cid)
        params = ParamsParser(request.JSON)
        try:
            with transaction.atomic():
                user = PracticeClassroomUser.objects.create(
                    author=self.auth.get_account(),
                    classroom=logic.classroom,
                    arrangement_id=params.int('arrangement', desc='排课id'),
                )
        except:
            raise PracticeClassroomUserExcept.classroomuser_create_fail()

        return SuccessResult(id=user.id)

    @check_login
    def delete(self, request, sid, cid, uid):
        """
        删除教室使用
        :param request:
        :param sid:
        :param cid:
        :param uid:
        :return:
        """
        logic = ClassroomLogic(self.auth, sid, cid)
        user = PracticeClassroomUser.objects.get_once(uid)
        if not user or user.classroom != logic.classroom:
            raise PracticeClassroomUserExcept.classroomuser_is_not_exists()

        user.delete()
        return SuccessResult(id=uid)