from django.urls import path, include
from .views import *


classification_urlpatterns = [
    path('', TaskClassificationInfoView.as_view(method=['POST'])),
    path('/<int:cid>', TaskClassificationInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/list', TaskClassificationListView.as_view(method=['GET'])),
]

apply_urlpatterns = [
    path('', TaskApplyInfoView.as_view(method=['POST'])),
    path('/<int:aid>', TaskApplyInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/list', TaskApplyListView.as_view(method=['GET'])),
]

urlpatterns = [
    path('', TaskInfoView.as_view(method=['POST'])),
    path('/list', TaskListView.as_view(method=['GET'])),
    path('/<int:tid>', TaskInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/classifications', include(classification_urlpatterns)),
    path('/<int:tid>/applies', include(apply_urlpatterns)),
]