"""maple_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from tokenize import Token
from django.contrib import admin
from django.urls import path, include
from .settings import dev
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/core/', include('core.urls')),
    path('api/location/', include('location.urls')),
    path('api/transaction/', include('transaction.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/file/', include('file.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if dev.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
