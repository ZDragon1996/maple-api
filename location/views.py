from cgitb import lookup
from django.shortcuts import render, get_list_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle
from .models import US_State, US_CITY
from .serializers import US_StateWithCitySerializer, US_StateSerializer
from rest_framework.mixins import ListModelMixin
from core.utils.utils import get_membership


# /location/state_list or /location/list_state: get
class CustomListAPIView(ListAPIView):
    throttle_classes = (ScopedRateThrottle,)

    def get_throttles(self):
        membership = get_membership(self.request)
        if membership:
            self.throttle_scope = membership
            print(membership)
        return super().get_throttles()


class US_StateListView(CustomListAPIView):
    def get_throttles(self):
        return super().get_throttles()

    def get_queryset(self):
        return US_State.objects.prefetch_related('cities').all()

    def get_serializer_class(self):
        return US_StateSerializer

    # def get_serializer_context(self):
    #     valid_mm_token = valid_membership_token(self.request)
    #     if valid_mm_token:
    #         self.throttle_scope = 'state_list_g'
    #         return {'membership_token': valid_mm_token}
    #     else:
    #         self.throttle_scope = 'state_list'
    #     return None

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
