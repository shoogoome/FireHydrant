# -*- coding: utf-8 -*-
# coding: utf-8

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...models import PracticeTag
from django.db.models import QuerySet

class PracticeTagListView(FireHydrantView):

    @check_login
    def get(self, request):
        """
        获取tag列表
        :param request:
        :return:
        """
        # TODO: 加入缓存
        # 尝试获取缓存数据
        # redis = WeJudgeCacheFactory(["education", "lesson", "list"])
        # data = redis.get_cache(str(cid))
        # if data:
        #     try:
        #         return SuccessResult(json.loads(data))
        #     except:
        #         pass

        all_tag = PracticeTag.objects.all()
        parent_lesson = all_tag.filter(parent__isnull=True).order_by('create_time')

        data = PracticeTagListView.get_tree_info(all_tag, parent_lesson, [])
        # 存储至缓存 1个月时间（因为在开始上课之后，正常来说课堂列表不发生变化）
        # try:
        #     redis.set_cache(str(cid), json.dumps(data), expired=2592000)
        # except:
        #     pass
        return SuccessResult(data)

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

