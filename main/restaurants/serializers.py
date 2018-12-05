from rest_framework import serializers

from restaurants.models import Restaurants


class RestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = ('id', 'name', 'type', 'phone', 'address')