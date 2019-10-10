# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logics.school import SchoolLogic
from ...models import PracticeSchool
from ...logics.classroom import ClassroomLogic
from ...logics.school import SchoolLogic
from ...models import PracticeClassroom
from ...models import PracticeClassroomUser
from common.exceptions.practice.classroom.user import PracticeClassroomUserExcept

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
        user = PracticeClassroomUser.objects.select_related(
            'account__account', 'practice__practicearrangement', 'practice__practiceclassroom'
        ).filter(
            classroom=logic.classroom
        ).values(
            'author', 'author__name', 'arrangement', 'arrangement__name',
            'classroom', 'classroom__name', 'create_time', 'update_time', 'id'
        )
        return SuccessResult([i for i in user])

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
        with transaction.atomic():
            try:
                user = PracticeClassroomUser.objects.create(
                    author=self.auth.get_account(),
                    classroom=logic.classroom,
                    arrangement_id=params.int('arrangement', desc='排课id'),
                )
            except Exception as ex:
                transaction.rollback()
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