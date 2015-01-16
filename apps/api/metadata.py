from rest_framework.metadata import SimpleMetadata, BaseMetadata
from rest_framework.utils.field_mapping import ClassLookupDict
from rest_framework import serializers
import fields


class ReportMetaData(SimpleMetadata):
    label_lookup = ClassLookupDict({
        serializers.Field: 'field',
        serializers.BooleanField: 'boolean',
        serializers.CharField: 'string',
        serializers.URLField: 'url',
        serializers.EmailField: 'email',
        serializers.RegexField: 'regex',
        serializers.SlugField: 'slug',
        serializers.IntegerField: 'integer',
        serializers.FloatField: 'float',
        serializers.DecimalField: 'decimal',
        serializers.DateField: 'date',
        serializers.DateTimeField: 'datetime',
        serializers.TimeField: 'time',
        serializers.ChoiceField: 'choice',
        serializers.MultipleChoiceField: 'multiple choice',
        serializers.FileField: 'file upload',
        serializers.ImageField: 'image upload',
        fields.PointField: "string",
    })

class AuthTokenMetaData(BaseMetadata):

    def determine_metadata(self, request, view):
        return {
            'name': view.get_view_name(),
            'description': view.get_view_description(),
            'actions': {
                'POST' : {
                    'email': {
                        'type': 'string',
                        'help_text': 'User email'
                    },
                    'password': {
                        'type': 'string',
                        'help_text': 'Password'
                    }
                }
            }
        }