from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
from file.custom_exceptions.exceptions import InvalidFileSizeException
from file.classes.csvfile import validate_source_file
from .serializers import ImageSerializer


# ==============================================================
# Custom APIView to restrict api calls for each user
# default membership: standard
# ==============================================================
class CustomViewSet(ModelViewSet):
    throttle_classes = (ScopedRateThrottle, UserRateThrottle)
    http_method_names = ['post']
    expected_type = ['.csv']

    def get_throttles(self):
        self.throttle_scope = 'image_limitation'
        return super().get_throttles()


# ==============================================================
# HTTP Allow: POST
# /api/file/image2sketch
# ==============================================================
class ImageViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = ImageSerializer
