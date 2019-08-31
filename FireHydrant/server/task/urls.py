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
    path('/list', TaskApplyManageView.as_view(method=['GET'])),
]

report_urlpatterns = [
    path('', TaskReportView.as_view(method=['POST'])),
    path('/<int:rid>', TaskReportView.as_view(method=['GET', 'DELETE', 'PUT'])),
]


urlpatterns = [
    path('', TaskInfoView.as_view(method=['POST'])),
    path('/list', TaskListView.as_view(method=['GET'])),
    path('/<int:tid>', TaskInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/classifications', include(classification_urlpatterns)),
    path('/<int:tid>/applies', include(apply_urlpatterns)),
    path('/<int:tid>/report', include(report_urlpatterns)),
]