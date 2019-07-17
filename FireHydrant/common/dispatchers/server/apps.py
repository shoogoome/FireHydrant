# -*- coding: utf-8 -*-
# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os
import celery
import raven
from raven.contrib.celery import register_signal, register_logger_signal
from django.conf import settings


# class Celery(celery.Celery):
#
#     def on_configure(self):
#         client = raven.Client(settings.WJ_CELERY_RAVEN_DSN)
#         # register a custom filter to filter out duplicate logs
#         register_logger_signal(client)
#         # hook into the Celery error handler
#         register_signal(client)
#

celery_app = celery.Celery("FireHydrant")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FireHydrant.settings')

celery_app.config_from_object('django.conf:settings', namespace='FIRE_CELERY')
celery_app.autodiscover_tasks()
