from django.urls import path, include
from .views import *

account_urlpatterns = [
    path('/login', FaceUAccountLogin.as_view(method=['POST'])),
    path('/develop/login', FireHydrantDevelopLogin.as_view(method=['POST'])),
    path('/<int:aid>', FaceUAccountInfoView.as_view(method=['GET', 'PUT'])),
    path('/list', FaceUAccountListMget.as_view(method=['GET'])),
    path('/_mget', FaceUAccountListMget.as_view(method=['POST'])),
]


urlpatterns = [
    path('/accounts', include(account_urlpatterns)),
]
