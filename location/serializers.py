from rest_framework import serializers
from .models import US_CITY, US_State


# City
class US_CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = US_CITY
        fields = ['city_name', 'county_name', 'latitude', 'longitude', 'state']


class US_DsiplayCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = US_CITY
        fields = ['city_name', 'county_name', 'latitude', 'longitude']

# State


class US_StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = US_State
        fields = ['state_code', 'state_name']


class US_StateWithCitySerializer(serializers.ModelSerializer):
    cities = US_DsiplayCitySerializer(many=True)

    # def create(self, validated_data):
    #     state_code = self.context['state_code']
    #     return US_State.objects.create(state_code=state_code, **validated_data)

    class Meta:
        model = US_State
        fields = ['state_code', 'state_name', 'cities']
