
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, CSV2TXTFileViewSet, XLSX2CSVFileViewSet
router = DefaultRouter()
router.register('csv2xlsx', FileViewSet, basename='file')
router.register('csv2txt', CSV2TXTFileViewSet, basename='file')
router.register('xlsx2csv', XLSX2CSVFileViewSet, basename='file')

urlpatterns = router.urls
