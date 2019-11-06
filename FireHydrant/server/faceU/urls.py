from django.urls import path, include
from .views import *

account_urlpatterns = [
    path('/login', FaceUAccountLogin.as_view(method=['POST'])),
    path('/<int:aid>', FaceUAccountInfoView.as_view(method=['GET'])),
]


urlpatterns = [
    path('/accounts', include(account_urlpatterns)),
]
