from os import stat
from django.http import HttpResponse
from django.shortcuts import render
from django.db import models
from django.http import HttpResponseNotFound
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from transaction.serializers import PaypalOrderSerializer
from django.core import serializers
from .models import PaypalOrder
from core.utils import utils
from copy import copy
# Create your views here.


class PaypalView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaypalOrderSerializer

    def get_queryset(self):
        return PaypalOrder.objects.all()

    def create(self, request, *args, **kwargs):
        response = utils.validate_paypal_transaction(request.data['order_id'])
        if response == 200:
            # set user id
            request.data['user_id'] = request.user.id

            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
