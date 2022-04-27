from django.shortcuts import render, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .serializers import US_StateWithCitySerializer, US_StateSerializer
from .models import US_State
from core.utils.utils import get_membership


# ==============================================================
# Custom APIView to restrict api calls for each user
# default membership: standard
# ==============================================================
class CustomListAPIView(ListAPIView):
    throttle_classes = (ScopedRateThrottle,)

    def get_throttles(self):
        membership = get_membership(self.request)
        if membership:
            self.throttle_scope = membership
            print(membership)
        return super().get_throttles()


# ==============================================================
# HTTP Allow: GET
# /api/location/states
# ==============================================================
class US_StateListView(CustomListAPIView):
    def get_throttles(self):
        return super().get_throttles()

    serializer_class = US_StateSerializer
    queryset = US_State.objects.prefetch_related('cities').all()

    #pagination_class = PageNumberPagination


# ==============================================================
# HTTP Allow: GET
# /api/location/states_and_cities
# ==============================================================
class US_StateWithCityLlistView(CustomListAPIView):

    @method_decorator(cache_page(86400 * 30))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    serializer_class = US_StateWithCitySerializer
    queryset = US_State.objects.prefetch_related('cities').all()


# ==============================================================
# HTTP Allow: GET
# /api/location/states/<state_code>
# ==============================================================
class US_StateWithCityDetailView(CustomListAPIView):
    serializer_class = US_StateWithCitySerializer

    @method_decorator(cache_page(86400 * 30))
    def get(self, request, *args, **kwargs):
        print(self.kwargs['state_code'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        print(self.kwargs['state_code'])
        return get_list_or_404(US_State, state_code=self.kwargs['state_code'])
