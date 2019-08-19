from django.urls import path, include
from .views import *

urlpatterns = [
    path('', AccountInfoView.as_view(method=['GET', 'PUT'], fetch_me=True)),
    path('/<int:aid>', AccountInfoView.as_view(method=['DELETE', 'GET', 'POST', 'PUT'])),
    path('/register', AccountRegisterView.as_view(method=['POST'])),
    path('/login', AccountLoginView.as_view(method=['POST', 'GET'])),
    path('/logout', AccountLogoutView.as_view(method=['POST'])),
    path('/list', AccountListView.as_view(method=['GET'])),
    path('/_mget', AccountInfoView.as_view(method=['POST'])),
    # Exhibition
    path('/<int:aid>/exhibitions', AccountExhibitionView.as_view(method=['POST'])),
    path('/<int:aid>/exhibitions/<int:eid>', AccountExhibitionView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/<int:aid>/exhibitions/list', AccountExhibitionListView.as_view(method=['GET'])),
]
