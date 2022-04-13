from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import ScopedRateThrottle
from .models import Customer, User
from .serializers import CustomerSerializer, UserSerializer

# Create your views here.


class CustomerViewSet(ModelViewSet):
    throttle_classes = (ScopedRateThrottle,)
    queryset = Customer.objects.select_related('user').all()
    serializer_class = CustomerSerializer
