from django.urls import path, include
from .views import *

urlpatterns = [

    path('/upload', ResourcesInfoView.as_view(method=['GET'], is_upload=True)),
    path('/download', ResourcesInfoView.as_view(method=['GET'])),
]