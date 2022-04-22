from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .models import Customer, User
from .serializers import CustomerSerializer, ImageSerializer
from rest_framework.response import Response
from .models import CustomerImage
from PIL import Image, ImageOps
from django.conf import settings
import os

# Create your views here.


class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    throttle_classes = (ScopedRateThrottle,)
    queryset = Customer.objects.select_related('user').all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        customer = get_object_or_404(Customer, user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CutomerImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer

    def get_serializer_context(self):
        return {'customer_id': self.kwargs['customer_pk']}

    def get_queryset(self):
        return CustomerImage.objects.filter(customer_id=self.kwargs['customer_pk'])

    def create(self, request, *args, **kwargs):
        print(os.path.join(
            settings.BASE_DIR, 'media', 'core', 'images'))
        path = os.path.join(
            settings.BASE_DIR, 'media', 'core', 'images')

        img = Image.open(os.path.join(path, 'test.png')).convert('RGBA')
        img_data = img.getdata()

        new_img_data = []
        for item in img_data:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                new_img_data.append((255, 255, 255, 0))
            else:
                new_img_data.append(item)

        img.putdata(new_img_data)
        img.save(os.path.join(path, 'new_img.png'), 'PNG')
        return super().create(request, *args, **kwargs)
