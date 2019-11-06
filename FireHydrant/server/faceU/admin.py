from django.contrib import admin
from .models import FaceUAccount, FaceUGroups, FaceUFacialMakeup, FaceUDistinguishRecord
# Register your models here.

admin.site.register(FaceUAccount)
admin.site.register(FaceUFacialMakeup)
admin.site.register(FaceUDistinguishRecord)
admin.site.register(FaceUGroups)
