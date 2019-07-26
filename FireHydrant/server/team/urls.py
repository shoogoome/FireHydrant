from django.urls import path, include
from .views import *


urlpatterns = [
    path('', TeamInfoView.as_view(method=['POST'])),
    path('/list', TeamListView.as_view(method=['GET'])),
    path('/<int:tid>', TeamInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/<int:tid>/join', TeamManageView.as_view(method=['POST'])),
    path('/<int:tid>/list', TeamManageView.as_view(method=['GET'])),
    # path('/<int:tid>/manage', TeamManageView.as_view(method=['PUT'])),
]
