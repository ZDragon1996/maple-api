from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle
from file.custom_decorators.decorators import handle_invalid_file
from .serializers import CSV2TXTSerializer, CSV2XLSXSerializer, TXT2CSVSerializer, XLSX2CSVSerializer, XLS2XLSXSerializer, TXT2XLSXSerializer
from django.conf import settings
from .classes.csvfile import CSVFile, validate_source_file
from .custom_exceptions.exceptions import InvalidFileSizeException
import os


# ==============================================================
# Custom APIView to restrict api calls for each user
# default membership: standard
# ==============================================================
class CustomViewSet(ModelViewSet):
    throttle_classes = (ScopedRateThrottle, UserRateThrottle)
    http_method_names = ['post']
    expected_type = ['.csv']

    def get_throttles(self):
        self.throttle_scope = 'file_limitation'
        return super().get_throttles()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if validate_source_file(file_name=request.data['file']._name, expected_type=self.expected_type):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            raise InvalidFileSizeException()


# ==============================================================
# HTTP Allow: POST
# /api/file/csv2xlsx
# ==============================================================
class CSV2XLSXViewSet(CustomViewSet):
    serializer_class = CSV2XLSXSerializer


# ==============================================================
# HTTP Allow: POST
# /api/file/csv2txt
# ==============================================================
class CSV2TXTFileViewSet(CustomViewSet):
    serializer_class = CSV2TXTSerializer


# ==============================================================
# HTTP Allow: POST
# /api/file/xlsx2csv
# ==============================================================
class XLSX2CSVFileViewSet(CustomViewSet):
    expected_type = ['.xlsx', '.xls']
    serializer_class = XLSX2CSVSerializer


# ==============================================================
# HTTP Allow: POST
# /api/file/xls2xlsx
# ==============================================================
class XLS2XLSXFileViewSet(CustomViewSet):
    serializer_class = XLS2XLSXSerializer
    expected_type = ['.xls']


# ==============================================================
# HTTP Allow: POST
# /api/file/txt2csv
# ==============================================================
class TXT2CSVFileViewSet(CustomViewSet):
    serializer_class = TXT2CSVSerializer
    expected_type = ['.txt']


# ==============================================================
# HTTP Allow: POST
# /api/file/txt2xlsx
# ==============================================================
class TXT2XLSXFileViewSet(TXT2CSVFileViewSet):
    serializer_class = TXT2XLSXSerializer
