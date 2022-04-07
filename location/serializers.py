from rest_framework import serializers
from .models import US_CITY, US_State


class US_StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = US_State
        fields = ['state_code', 'state_name']


class US_CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = US_CITY
        fields = ['city_name', 'county_name', 'latitude', 'longitude', 'state']
