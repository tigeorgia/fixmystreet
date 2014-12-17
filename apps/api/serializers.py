from rest_framework import serializers, exceptions

from apps.api import fields
from apps.mainapp.models import Report, Ward, ReportCategory
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


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
    ward__city = serializers.IntegerField(source='ward.city.id', read_only=True)
    # TODO convert photo to stdimagefield

    class Meta:
        model = Report
        fields = ('id', 'title', 'category', 'ward', 'ward__city', 'created_at', 'updated_at', 'status', 'street', 'fixed_at',
                  'sent_at', 'email_sent_to', 'coordinates', 'desc',
        )
        read_only_fields = ('id', 'sent_at', 'ward', 'created_at', 'updated_at', 'fixed_at', 'email_sent_to',)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs