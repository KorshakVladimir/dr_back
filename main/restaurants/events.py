import json

from main.wsgi import sio
from restaurants.models import Restaurants
from restaurants.serializers import RestaurantsSerializer


@sio.on('remove_table_row')
def remove_table_row_event(sid, id):
    rest_instance = Restaurants.objects.get(pk=id)
    rest_instance.delete()


@sio.on('update_table_row')
def update_table_row_event(sid, data):
    rest_instance = Restaurants.objects.get(pk=data['id'])
    serializer = RestaurantsSerializer(rest_instance, data=data)
    if serializer.is_valid():
        serializer.save()


@sio.on('update_table')
def update_table_event(sid):
    get_restaurants()


def get_restaurants():
    restaurants = Restaurants.objects.all()
    serializer = RestaurantsSerializer(restaurants, many=True)
    sio.emit('init_table', serializer.data)