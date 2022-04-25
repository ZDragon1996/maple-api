from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from requests import post
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet
from file.custom_decorators.decorators import handle_invalid_file
from .serializers import CSV2TXTSerializer, FileSerializer, XLSX2CSVSerializer
from django.conf import settings
from rest_framework.decorators import action
import os
from .process_file import download_file
# Create your views here.


class FileViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = FileSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    @handle_invalid_file
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class CSV2TXTFileViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = CSV2TXTSerializer

    @handle_invalid_file
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class XLSX2CSVFileViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = XLSX2CSVSerializer

    @handle_invalid_file
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)