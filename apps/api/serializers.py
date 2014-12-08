from rest_framework import serializers

from apps.api import fields
from apps.mainapp.models import Report, Ward, ReportCategory


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportCategory
        fields = ('id',)


class WardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ward
        fields = ('id', 'name', 'city')


class ReportSerializer(serializers.ModelSerializer):
    coordinates = fields.PointField(source='point',)
    # TODO convert photo to stdimagefield

    class Meta:
        model = Report
        fields = ('id', 'title', 'category', 'ward', 'created_at', 'updated_at', 'status', 'street', 'fixed_at',
                  'sent_at', 'email_sent_to', 'coordinates', 'desc',
        )
        read_only_fields = ('id', 'sent_at', 'created_at', 'updated_at', 'fixed_at', 'email_sent_to',)