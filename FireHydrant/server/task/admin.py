from django.contrib import admin
from .models import Task, TaskReport, TaskClassification
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskReport)
admin.site.register(TaskClassification)