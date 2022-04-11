from django.shortcuts import render
from django.db import models
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from transaction.serializers import PaypalOrderSerializer
from django.core import serializers
from .models import PaypalOrder
# Create your views here.


class PaypalView(ListCreateAPIView):

    def get_queryset(self):
        return PaypalOrder.objects.all()

    serializer_class = PaypalOrderSerializer
