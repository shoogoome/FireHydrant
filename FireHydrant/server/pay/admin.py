from django.contrib import admin
from .models import PayAccount
from .models import PayRecord
# Register your models here.

admin.site.register(PayRecord)
admin.site.register(PayAccount)





