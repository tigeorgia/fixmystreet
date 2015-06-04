from django.conf import settings
from rest_framework import serializers, exceptions
from django.template.loader import render_to_string
from django.core.mail import send_mail
from apps.api import fields
from apps.mainapp.models import Report, ReportUpdate, Ward, ReportCategory, City, FaqEntry, ReportPhoto
from apps.users.models import FMSUser
from django.contrib.auth import authenticate
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _


EXCEPTIONS = {
    'no-permission-report': exceptions.PermissionDenied(_('You are not allowed to modify this report')),
    'no-permission-report-status': exceptions.PermissionDenied(_('Only city councillors and report creators can update report status')),
    'no-permission-general': exceptions.PermissionDenied(_('You are not allowed to perform this action')),
    'report-not-found': exceptions.ValidationError(_('Report with this ID does not exist')),
    'user-disabled': exceptions.ValidationError(_('User account is disabled.')),
    'incorrect-credentials': exceptions.ValidationError(_('Unable to log in with provided credentials.')),
    'email-pass-required': exceptions.ValidationError(_('Must include "email" and "password"')),
    'ward-not-found': exceptions.ValidationError(_("Provided location doesn't belong to any of the available cities"))
}

class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    """
    class Meta:
        model = ReportCategory
        fields = ('id', 'name')


class CitySerializer(serializers.ModelSerializer):
    """
    City serializer
    """
    class Meta:
        model = City
        fields = ('id', 'name')


class WardSerializer(serializers.ModelSerializer):
    """
    Ward serializer
    """
    city = CitySerializer(read_only=True)

    class Meta:
        model = Ward
        fields = ('id', 'name', 'city')


class FaqEntrySerializer(serializers.ModelSerializer):
    """
    FAQ serializer
    """
    class Meta:
        model = FaqEntry
        fields = ('id', 'order', 'q_en', 'a_en', 'q_ka', 'a_ka')

class ContactSerializer(serializers.Serializer):
    """
    Contact serializer
    """
    name = serializers.CharField()
    email = serializers.EmailField()
    body = serializers.CharField()

    def save(self, **kwargs):
        """
        Override save() method in order to send an email
        """
        message = render_to_string("emails/contact/message.txt", self.data)
        send_mail('FixMyStreet.ge User Message from %s' % self.data['email'], message,
                  settings.EMAIL_FROM_USER, [settings.ADMIN_EMAIL], fail_silently=False)


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    class Meta:
        model = FMSUser
        fields = ('id', 'username', 'first_name', 'last_name', 'is_councillor')


class ExtendedUserSerializer(serializers.ModelSerializer):
    """
    User serializer containing more data. Used for authenticated users,
    so that only they can access private information
    """
    date_joined = fields.UnixTimeReadOnlyField()

    class Meta:
        model = FMSUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'phone', 'date_joined', 'is_councillor', 'is_staff', 'is_confirmed', 'is_active')


class ReportPhotoSerializer(serializers.ModelSerializer):
    photo = fields.StdImageField(required=True)
    report_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        report_id = int(validated_data.pop('report_id'))
        user = self.context['request'].user

        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            raise EXCEPTIONS['report-not-found']

        if not user.can_upload_photo(report=report):
            raise EXCEPTIONS['no-permission-report']

        return ReportPhoto.objects.create(report=report, **validated_data)

    class Meta:
        model = ReportPhoto
        fields = ('id', 'report_id', 'order', 'photo')

class ReportSerializer(serializers.ModelSerializer):
    """
    Report serializer
    """
    longitude = serializers.FloatField(source='point.x')
    latitude = serializers.FloatField(source='point.y')
    fixed_at = fields.UnixTimeReadOnlyField()
    created_at = fields.UnixTimeReadOnlyField()
    updated_at = fields.UnixTimeReadOnlyField()
    sent_at = fields.UnixTimeReadOnlyField()
    user = UserSerializer(read_only=True)
    report_photos = ReportPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = (
            'id', 'title', 'category', 'ward', 'has_photo', 'report_photos', 'created_at', 'updated_at', 'status', 'street', 'fixed_at',
            'sent_at', 'email_sent_to', 'longitude', 'latitude', 'desc', 'user',
        )
        read_only_fields = ('id', 'status', 'ward', 'fixed_at', 'email_sent_to')

    @staticmethod
    def generate_point(x, y):
        """
        Return GIS supported Point object from x and y values
        """
        return Point(x, y, srid=4326)

    def create(self, validated_attrs):
        """
        Override create() method in order to attach Ward to Report
        """
        point = self.generate_point(validated_attrs['point']['x'], validated_attrs['point']['y'])
        validated_attrs['point'] = point
        try:
            ward = Ward.objects.get(geom__contains=point)
        except Ward.DoesNotExist:
            raise EXCEPTIONS['ward-not-found']
        user = self.context['request'].user
        return Report.objects.create(user=user, ward=ward, **validated_attrs)


class ReportUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_at = fields.UnixTimeReadOnlyField()
    updated_at = fields.UnixTimeReadOnlyField()
    report_id = serializers.IntegerField()

    def create(self, validated_data):
        report_id = int(validated_data.pop('report_id'))
        user = self.context['request'].user

        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            raise EXCEPTIONS['report-not-found']

        if not report.status == validated_data.get('status'):
            if not user.can_update_report(report):
                raise EXCEPTIONS['no-permission-report-status']

        return ReportUpdate.objects.create(report=report, user=user, **validated_data)

    class Meta:
        model = ReportUpdate
        fields = ('id', 'report_id', 'user', 'status', 'created_at', 'updated_at', 'desc')

