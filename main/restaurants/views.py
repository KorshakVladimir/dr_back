from django.http import JsonResponse
from rest_framework import views
from rest_framework.parsers import FileUploadParser, MultiPartParser
import json
from main.wsgi import sio
from restaurants.events import get_restaurants
from restaurants.serializers import RestaurantsSerializer
from main.local_settings import GEO_KEY

import concurrent.futures
import urllib.request


def load_url(url):
    with urllib.request.urlopen(url, timeout=2) as conn:
        return conn.read()


class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser,)

    def _csv_to_json(self, data):
        data_json = []
        column_names = data[0].split(',')
        for row in data[1:]:
            if not row:
                continue
            restaurant = {}
            row_list = row.split(',')
            for counter, column in enumerate(column_names):
                restaurant[column.lower()] = row_list[counter]
            data_json.append(restaurant)
        return data_json

    @staticmethod
    def create_restaurants(data):
        location_geo = data['location'].split('/')
        response = load_url('https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}'
                            .format(location_geo[0], location_geo[1], GEO_KEY))
        data['address'] = json.loads(response)['results'][0]['formatted_address']
        serializer = RestaurantsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

    def post(self, request):
        file_obj = request.data['file']
        try:
            data = self._csv_to_json(file_obj.file.getvalue().decode().split("\r\n"))
        except:
            return JsonResponse({"file parser error"}, status=400)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.create_restaurants, restaurant_el) for restaurant_el in data}
            concurrent.futures.as_completed(future_to_url)
        for i in data:
            self.create_restaurants(i)
        get_restaurants()
        return JsonResponse("ok", status=201, safe=False)
