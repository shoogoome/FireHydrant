from django.urls import path, include
from .views import *

account_urlpatterns = [
    path('/login', FaceUAccountLogin.as_view(method=['POST'])),
    path('/develop/login', FireHydrantDevelopLogin.as_view(method=['POST'])),
    path('/<int:aid>', FaceUAccountInfoView.as_view(method=['GET', 'PUT'])),
    path('/list', FaceUAccountListMget.as_view(method=['GET'])),
    path('/_mget', FaceUAccountListMget.as_view(method=['POST'])),
]


group_urlpatterns = [
    path('', FaceUGroupInfo.as_view(method=['POST'])),
    path('/<int:gid>', FaceUGroupInfo.as_view(method=['GET', 'DELETE', 'PUT'])),
    path('/<int:gid>/list', FaceUGroupListMget.as_view(method=['GET'])),
    path('/<int:gid>/_mget', FaceUGroupListMget.as_view(method=['POST'])),
    path('/<int:gid>/manage', FaceUGroupManageView.as_view(method=['GET', 'POST', 'DELETE'])),
    path('/<int:gid>/manage/_mpost', FaceUGroupManageMany.as_view(method=['POST'])),
    path('/<int:gid>/manage/<int:mid>', FaceUGroupManageView.as_view(method=['PUT']))
]


urlpatterns = [
    path('/accounts', include(account_urlpatterns)),
    path('/groups', include(group_urlpatterns)),
]
