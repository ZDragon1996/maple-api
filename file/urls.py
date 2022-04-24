
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, CSV2TXTFileViewSet
router = DefaultRouter()
router.register('file/csv2xlsx', FileViewSet, basename='file')
router.register('file/csv2txt', CSV2TXTFileViewSet, basename='file')

urlpatterns = router.urls
