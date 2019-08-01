from django.urls import path, include
from .views import *


classification_urlpatterns = [
    path('', TaskClassificationInfoView.as_view(method=['POST'])),
    path('/<int:cid>', TaskClassificationInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/list', TaskClassificationListView.as_view(method=['GET'])),
]

urlpatterns = [
    path('/classifications', include(classification_urlpatterns)),
    path('', TaskInfoView.as_view(method=['POST'])),
    path('/<int:tid>', TaskInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/list', TaskListView.as_view(method=['GET'])),
]