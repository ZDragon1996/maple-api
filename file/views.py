from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from requests import post
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle
from file.custom_decorators.decorators import handle_invalid_file
from .serializers import CSV2TXTSerializer, FileSerializer, XLSX2CSVSerializer
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

    def get_throttles(self):
        self.throttle_scope = 'file_limitation'
        return super().get_throttles()


class FileViewSet(CustomViewSet):
    http_method_names = ['post']
    serializer_class = FileSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CSV2TXTFileViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = CSV2TXTSerializer

    def create(self, request, *args, **kwargs):
        print()
        return super().create(request, *args, **kwargs)


class XLSX2CSVFileViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = XLSX2CSVSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if validate_source_file(file_name=request.data['file']._name, expected_type=['.xlsx', '.xls']):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            raise InvalidFileSizeException()
