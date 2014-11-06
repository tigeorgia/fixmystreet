from rest_framework import serializers


class Point(object):
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat


class PointField(serializers.WritableField):
    point_type = None
    points = {'lon': '', 'lat': ''}

    def __init__(self, point_type, *args, **kwargs):
        super(PointField, self).__init__(*args, **kwargs)
        self.point_type = point_type

    def get_point(self):
        return self.points[self.point_type]

    def set_point(self, lon, lat):
        self.points['lon'] = lon
        self.points['lat'] = lat

    def to_native(self, value):
        value = str(value).strip("POINT ()").split(" ")
        lon, lat = value
        self.set_point(lon, lat)
        return self.get_point()

    def from_native(self, value):
        value = value.strip("POINT ()").split(" ")
        lon, lat = value
        return Point(lon, lat)