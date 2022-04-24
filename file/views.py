from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from requests import post
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet
from .models import File
from .serializers import CSV2TXTSerializer, FileSerializer
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

    def create(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CSV2TXTFileViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = CSV2TXTSerializer

    def create(self, request, *args, **kwargs):
        serializer = CSV2TXTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
