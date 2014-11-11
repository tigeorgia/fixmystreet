from rest_framework import serializers
import fields

from mainapp.models import Report


class ReportSerializer(serializers.ModelSerializer):
    coordinates = fields.PointField(source='point')
    photo = serializers.ImageField(source='photo')  # TODO convert this to stdimagefield

    class Meta:
        model = Report
        fields = ('title', 'author', 'category', 'ward', 'created_at', 'updated_at', 'street', 'updated_at', 'fixed_at',
                  'sent_at', 'email_sent_to', 'coordinates', 'photo',
                  'desc'
        )
        read_only_fields = ('ward', 'sent_at', 'created_at', 'updated_at', 'fixed_at', 'email_sent_to',)