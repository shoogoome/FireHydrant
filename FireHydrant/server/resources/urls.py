from django.urls import path, include
from .views import *

urlpatterns = [

    # path('/upload/<int:mid>', ResourcesInfoView.as_view(method=['GET'], is_upload=True)),
    # path('/download/<int:mid>', ResourcesInfoView.as_view(method=['GET'])),
]