"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import incßßlude, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.ußßrls'))
"""
from django.contrib import admin
from django.urls import path, include
from store.views import multiply

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),  # Добавили эту строчку
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts_allauth/", include("allauth.urls")),  # Подключили allauth
    path('pages/', include('django.contrib.flatpages.urls')),
    # Делаем так, чтобы все адреса из нашего приложения (store/urls.py) подключались к главному приложению с префиксом products/.
    path('store/', include('store.urls')),
    path('newsportal/', include('newsportal.urls')),
    path('multiply/', multiply),
    path('mc_board/', include('mc_board.urls')),
]
