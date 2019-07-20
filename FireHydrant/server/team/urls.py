from django.urls import path, include
from .views import *


urlpatterns = [
    path('', TeamInfoView.as_view(method=['POST'])),
    path('/<int:tid>', TeamInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
]
