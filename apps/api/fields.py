from collections import OrderedDict
from decimal import Decimal

from rest_framework import serializers
from django.contrib.gis.geos import Point


class PointField(serializers.WritableField):

    def __init__(self, *args, **kwargs):
        self.points = OrderedDict([('longitude', None), ('latitude', None)])
        super(PointField, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        self.points.update({'longitude': obj.x, 'latitude': obj.y})
        return self.points

    def from_native(self, value):
        lonlat = [Decimal(x.strip()) for x in value.split(',')]
        return Point(lonlat)
