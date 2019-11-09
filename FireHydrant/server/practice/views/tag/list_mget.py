# -*- coding: utf-8 -*-
# coding: utf-8

from common.core.auth.check_login import check_login
from common.core.http.firehydrant import FireHydrantView
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...models import PracticeTag
from django.db.models import QuerySet
from ...logics.factory import TagRedisClusterFactory

class PracticeTagListView(FireHydrantView):

    @check_login
    def get(self, request):
        """
        获取tag列表
        :param request:
        :return:
        """
        data = self.get_data()
        return SuccessResult(data)

    def get_data(self):
        """
        获取tag信息
        :return:
        """
        # 尝试获取缓存
        cache = TagRedisClusterFactory()
        if cache.exists("all"):
            return cache.get_json("all")

        all_tag = PracticeTag.objects.all()
        parent_lesson = all_tag.filter(parent__isnull=True).order_by('create_time')

        data = PracticeTagListView.get_tree_info(all_tag, parent_lesson, [])
        # 缓存数据
        cache.set_json("all", data)
        return data

    @staticmethod
    def get_tree_info(all_tag: QuerySet, tags: QuerySet, data: list) -> list:
        """
        获取树形课程信息
        :param all_tag:
        :param tags:
        :param data:
        :return:
        """
        for tag in tags:
            children_lesson = all_tag.filter(parent=tag).order_by('create_time')
            try:
                info = {
                    'id': tag.id,
                    'name': tag.name,
                    'create_time': tag.create_time,
                }
                if children_lesson.exists():
                    info['children'] = PracticeTagListView.get_tree_info(all_tag, children_lesson, [])
                data.append(info)
            except Exception as e:
                raise e
                pass
        return data

