
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FileViewSet
router = DefaultRouter()
router.register('file', FileViewSet, basename='file')

urlpatterns = router.urls
