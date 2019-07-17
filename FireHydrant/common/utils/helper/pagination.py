# -*- coding: utf-8 -*-
# coding:utf-8
from django.db import models


def slicer_default_func(obj, *args, **kwargs):
    return obj

def slicer(instance, limit=10, page=1):
    """
    实现分页系统的装饰器
    :param instance:    Queryset对象
    :type instance:     models.QuerySet
    :param limit:       每页显示记录数
    :param page:        当前第几页
    :return:

    data, pagination
    处理过的列表，分页信息

    pagination = {
        "page": 6,                      // 当前页数
        "total": 1000,                  // 总记录数
        "limit": 50,                    // 单页限制记录数
    }

    """
    def decorator(func=slicer_default_func):

        def wrapper(*args, **kwargs):
            # 处理分页数据
            _page = page if page > 0 else 1
            _limit = limit if limit > 0 else 1
            # 获取记录总数
            total = instance.count() if isinstance(instance, models.QuerySet) else len(instance)
            # 构造分页数据
            pagination = {
                "page": _page,
                "limit": _limit,
                "total": total
            }
            if total == 0:
                return list(), pagination

            # 获取记录起点索引
            start_idx = _limit * (_page - 1)
            # 切割实体数据
            data = [func(obj, *args, **kwargs) for obj in instance[start_idx: start_idx + _limit]]
            return data, pagination

        return wrapper

    return decorator

