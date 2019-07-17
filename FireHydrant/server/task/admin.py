from django.contrib import admin
from .models import Task, TaskReport
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskReport)