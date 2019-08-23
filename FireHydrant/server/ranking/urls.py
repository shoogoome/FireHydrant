from django.urls import path, include
from .views import *

urlpatterns = [
    path('/task', RankingTaskView.as_view(method=['GET'])),
]
