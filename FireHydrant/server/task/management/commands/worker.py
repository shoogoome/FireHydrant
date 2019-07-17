# -*- coding: utf-8 -*-
# coding:utf-8
from __future__ import absolute_import, unicode_literals
from django.core.management.base import BaseCommand
from common.dispatchers.server import celery_app

INTERPRETER = "/usr/bin/python"

class Command(BaseCommand):

    def handle(self, *args, **options):
        celery_app.worker_main(['worker.py', '-l', 'info'])