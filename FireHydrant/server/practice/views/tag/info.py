# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logics.school import SchoolLogic
from ...models import PracticeSchool
from ...models import PracticeTag
from common.exceptions.practice.tag.info import PracticeTagInfoExcept
from ...logics.tag import TagLogic

class PracticeTagView(FireHydrantView):

    @check_login
    def post(self, request):
        """
        创建tag
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        name = params.str('name', desc='名称')
        if PracticeTag.objects.filter(name=name).exists():
            raise PracticeTagInfoExcept.tag_name_is_exists()

        if params.has('parent'):
            parent = PracticeTag.objects.get_once(params.int('parent', desc='父节点id'))
            if not parent:
                raise PracticeTagInfoExcept.parent_is_not_exists()

        tag = PracticeTag.objects.create(
            name=params.str('name', desc='名称'),
        )
        # 这里无需判断是否环形，因为新建节点肯定不会出现环形情况
        if params.has('parent'):
            tag.parent = parent
        tag.save()
        return SuccessResult(id=tag.id)

    @check_login
    def get(self, request, tid):
        """
        获取tag信息
        :param request:
        :param tid:
        :return:
        """
        logic = TagLogic(self.auth, tid)
        return SuccessResult(logic.get_tag_info())

    @check_login
    def put(self, request, tid):
        """
        修改tag信息
        :param request:
        :param tid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = TagLogic(self.auth, tid)

        tag = logic.tag
        if params.has('parent'):
            # 判断是否非法操作(是否环形)
            parent = PracticeTag.objects.get_once(params.int('parent', desc='父节点id'))
            if parent and TagLogic.is_not_annular(parent, tag.id):
                tag.parent = parent
            else:
                raise PracticeTagInfoExcept.parent_appoint_illegal()
        with params.diff(tag):
            tag.name = params.str('name', desc='名称')
        tag.save()
        return SuccessResult(id=tid)

    @check_login
    def delete(self, request, tid):
        """
        删除tag
        :param request:
        :param tid:
        :return:
        """
        logic = TagLogic(self.auth, tid)
        logic.tag.delete()

        return SuccessResult(id=tid)