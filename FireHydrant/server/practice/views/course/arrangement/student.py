# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from common.enum.practice.oddeven import OddEvenEnum
from common.exceptions.practice.course.arrangement import PracticeArrangementInfoExcept
from ....logics.arrangement import ArrangementLogic
from ....logics.course import CourseLogic
from ....models import PracticeStudentUser
from ....models import PracticeArrangement
from ....logics.student import StudentUserLogic

class PracticeArrangementStudentInfoView(FireHydrantView):

    @check_login
    def post(self, request, sid, cid, aid):
        """
        批量导入学生信息
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        logic = ArrangementLogic(self.auth, sid, cid, aid)
        slogic = StudentUserLogic(self.auth, sid)
        params = ParamsParser(request.JSON)
        studentuser_data = params.list('data', desc='导入学生信息')

        arrangement = logic.arrangement
        for data in studentuser_data:
            data_params = ParamsParser(data)
            try:
                studentuser = slogic.create_studentuser(data_params)
                arrangement.students.add(studentuser)
            except:
                pass
        arrangement.save()

        return SuccessResult(id=aid)

    @check_login
    def delete(self, request, sid, cid, aid):
        """
        批量移除学生
        :param request:
        :param sid:
        :param cid:
        :param aid:
        :return:
        """
        logic = ArrangementLogic(self.auth, sid, cid, aid)
        params = ParamsParser(request.JSON)
        ids = params.list('ids', desc='id列表')

        studentuser = PracticeStudentUser.objects.get_many(ids)
        for i in studentuser:
            logic.arrangement.student.remove(i)
        logic.arrangement.save()

        return SuccessResult(id=aid)

