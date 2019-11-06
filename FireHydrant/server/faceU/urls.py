from django.urls import path, include
from .views import *

account_urlpatterns = [
    path('/login', FaceUAccountLogin.as_view(method=['POST'])),
]


urlpatterns = [
    path('/accounts', include(account_urlpatterns)),
]
