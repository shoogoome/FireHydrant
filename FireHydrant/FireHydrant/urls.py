"""FireHydrant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from server.account.urls import urlpatterns as account_urlpatterns
from server.team.urls import urlpatterns as team_urlpatterns
from server.task.urls import urlpatterns as task_urlpatterns
from server.resources.urls import urlpatterns as resources_urlpatterns

urlpatterns = [
    path('server_admin/', admin.site.urls),
    path('accounts', include(account_urlpatterns)),
    path('teams', include(team_urlpatterns)),
    path('tasks', include(task_urlpatterns)),
    path('resources', include(resources_urlpatterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
