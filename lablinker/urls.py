"""
URL configuration for lablinker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path

BASE_URL = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{BASE_URL}/auth/', include('auth_app.urls')),
    path(f'{BASE_URL}/users/', include('user.urls')),
    path(f'{BASE_URL}/posts/', include('posts.urls')),
    path(f'{BASE_URL}/likes/', include('likes.urls')),
    path(f'{BASE_URL}/comments/', include('comments.urls')),
    path(f'{BASE_URL}/resources/', include('resources.urls')),
]
