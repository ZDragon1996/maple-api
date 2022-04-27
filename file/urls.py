
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CSV2XLSXViewSet, CSV2TXTFileViewSet, TXT2CSVFileViewSet, XLS2XLSXFileViewSet, XLSX2CSVFileViewSet, TXT2XLSXFileViewSet
router = DefaultRouter()
router.register('csv2xlsx', CSV2XLSXViewSet, basename='file')
router.register('csv2txt', CSV2TXTFileViewSet, basename='file')
router.register('xlsx2csv', XLSX2CSVFileViewSet, basename='file')
router.register('xls2csv', XLSX2CSVFileViewSet, basename='file')
router.register('xls2xlsx', XLS2XLSXFileViewSet, basename='file')
router.register('txt2csv', TXT2CSVFileViewSet, basename='file')
router.register('txt2xlsx', TXT2XLSXFileViewSet, basename='file')
urlpatterns = router.urls
