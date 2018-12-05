from django.db import models


class Restaurants(models.Model):
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=200)
    phone = models.CharField(max_length=8)
    location = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
