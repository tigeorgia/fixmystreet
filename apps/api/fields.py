from rest_framework import serializers
from time import mktime
from arrow.arrow import Arrow
import dateutil.parser


class StdImageField(serializers.ImageField):
    def __init__(self, *args, **kwargs):
        super(StdImageField, self).__init__(*args, **kwargs)

    def get_variations(self, value):
        stdimagefield = value.field
        variations = {}
        if hasattr(stdimagefield, 'variations'):
            for name, variation in stdimagefield.variations.iteritems():
                if hasattr(value, name):
                    variations[name] = variation
                    variations[name]['url'] = getattr(value, name).url
        return variations if variations else None

    def to_representation(self, value):
        variations = self.get_variations(value)
        return variations

    def to_internal_value(self, data):
        return super(StdImageField, self).to_internal_value(data)


class EpochTimeReadOnlyField(serializers.ReadOnlyField):

    def to_representation(self, value):
        epoch_utc = int(mktime(value.timetuple()))
        return epoch_utc
