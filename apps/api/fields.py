from collections import OrderedDict
from decimal import Decimal

from rest_framework import serializers
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _


class PointField(serializers.Field):

    def __init__(self, *args, **kwargs):
        super(PointField, self).__init__(*args, **kwargs)
        self.points = OrderedDict([('longitude', None), ('latitude', None)])
        self.help_text = _("Longitude and Latitude in string format. Separated by comma. "
                           "Example: '44.7965081557,41.708484'")

    def to_representation(self, obj):
        self.points.update({'longitude': obj.x, 'latitude': obj.y})
        return self.points

    def to_internal_value(self, value):
        lonlat = [Decimal(x.strip()) for x in value.split(',')]
        try:
            point = Point(lonlat)
        except TypeError:
            raise serializers.ValidationError('Point field should be Longitude and Latitude string, separated by comma')
        return point
