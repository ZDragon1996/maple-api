from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import US_State, US_CITY
from .serializers import US_CitySerializer, US_StateSerializer


# Create your views here.
@api_view(['get'])
def get_state(request):
    queryset = US_State.objects.all()
    serializer = US_StateSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['get'])
def get_city(request):
    queryset = US_CITY.objects.all()
    serializer = US_CitySerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
