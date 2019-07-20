from django.urls import path, include
from .views import *

urlpatterns = [
    path('', AccountInfoView.as_view(method=['GET', 'PUT'], fetch_me=True)),
    path('/<int:aid>', AccountInfoView.as_view(method=['DELETE', 'GET', 'POST', 'PUT'])),
    path('/register', AccountRegisterView.as_view(method=['POST'])),
    path('/login', AccountLoginView.as_view(method=['POST'])),
    path('/list', AccountListView.as_view(method=['GET'])),
    path('/_mget', AccountInfoView.as_view(method=['POST'])),
]
