from rest_framework import serializers
import fields

from mainapp.models import Report


class ReportSerializer(serializers.ModelSerializer):
    ip = serializers.Field(source='ip')
    is_hate = serializers.Field(source='is_hate')
    sent_at = serializers.DateTimeField(source='sent_at', read_only=True)
    created_at = serializers.DateTimeField(source='created_at', read_only=True)
    updated_at = serializers.DateTimeField(source='updated_at', read_only=True)
    fixed_at = serializers.DateTimeField(source='fixed_at', read_only=True)
    email_sent_to = serializers.EmailField(source='email_sent_to', read_only=True)
    reminded_at = serializers.DateTimeField(source='reminded_at', read_only=True)
    longitude = fields.PointField(source='point', point_type='lon')
    latitude = fields.PointField(source='point', point_type='lat')
    photo = serializers.ImageField('photo')

    class Meta:
        model = Report
        fields = ('title', 'author', 'category', 'ward', 'ip', 'created_at', 'updated_at', 'street', 'updated_at', 'fixed_at', 'status',
                  'sent_at', 'email_sent_to', 'reminded_at', 'longitude', 'latitude', 'photo', 'desc'
        )