# -*- coding: utf-8 -*-
# coding:utf-8

import time
from django.db import models


class TimeStampField(models.FloatField):
    """
    时间戳Field
    """

    description = "TimeStamp using Floating point number"

    def __init__(self, verbose_name=None, name=None, auto_now=False,
                 auto_now_add=False, **kwargs):
        self.auto_now, self.auto_now_add = auto_now, auto_now_add
        if auto_now or auto_now_add:
            kwargs['null'] = False
            kwargs['blank'] = False
            kwargs['default'] = 0
        super().__init__(verbose_name, name, **kwargs)

    def get_internal_type(self):
        return "FloatField"

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = time.time()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)