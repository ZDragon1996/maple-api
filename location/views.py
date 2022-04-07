from cgitb import lookup
from django.shortcuts import render, get_list_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import ScopedRateThrottle
from .models import US_State, US_CITY
from .serializers import US_StateWithCitySerializer, US_StateSerializer


# /location/state_list : get
class US_StateListView(ListAPIView):
    throttle_scope = 'state_list'
    throttle_classes = (ScopedRateThrottle,)

    def get_queryset(self):
        return US_State.objects.prefetch_related('cities').all()

    def get_serializer_class(self):
        return US_StateSerializer

    #pagination_class = PageNumberPagination


# /location/states : get
# loading might take long time, using caching in the future
class US_StateWithCityLlistView(ListAPIView):
    def get_queryset(self):
        return US_State.objects.prefetch_related('cities').all()

    def get_serializer_class(self):
        return US_StateWithCitySerializer


# /location/states/<state_code> : get
class US_StateWithCityDetailView(ListAPIView):
    def get_queryset(self):
        return get_list_or_404(US_State, state_code=self.kwargs['state_code'])

    def get_serializer_class(self):
        return US_StateWithCitySerializer

    def get_serializer_context(self):
        return {'state_code': self.kwargs['state_code']}
