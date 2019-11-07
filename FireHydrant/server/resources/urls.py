from django.urls import path, include
from .views import *

urlpatterns = [
    # 本地全局资源下载
    path('/<str:token>', FireHydrantLocalResourceView.as_view(method=['GET'])),
    # 获取上传路由
    path('/upload/token', ResourcesInfoView.as_view(method=['GET'])),
    # 完成上传
    path('/upload/finish', ResourcesInfoView.as_view(method=['POST'])),
]

