from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse as dj_reverse
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse as reverse
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.decorators import renderer_classes
from django.http import Http404
from collections import OrderedDict

from apps.mainapp.models import Report, Ward, ReportCategory, FaqEntry
from apps.mainapp.utils import ReportCount
from apps.mainapp.filters import ReportFilter
from .serializers import ReportSerializer, WardSerializer, AuthTokenSerializer, CategorySerializer, FaqEntrySerializer,\
    ContactSerializer, ExtendedUserSerializer
from metadata import AuthTokenMetaData, ReportCountMetadata
from apps.users.models import FMSUserAuthToken
from apps.mainapp.forms import ContactForm
from django.contrib.gis.measure import D
from django.contrib.gis.geos import fromstr
from time import mktime
from arrow import Arrow
import datetime
import pytz

class LoginRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        redirect_url = reverse('home')

        if 'api' in self.request.path:
            redirect_url = reverse('api:report-list')

        elif self.request.user.is_staff:
            redirect_url = reverse('admin')

        return redirect_url


class APIRootView(APIView):
    """
    This is chemikucha API root.

    For full access, you'll need to get authentication token.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:

    `Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a`

    You need to generate the token once. If you want to generate authorization token using 3rd
    party service (facebook),

    # Endpoints:

    ___

    ## Authorization:
    * **Obtain token**: [/api/auth/token/](/api/auth/token/)

        This endpoint allows you to generate auth token using email & password or using refresh_token

        * Allowed methods

            * `POST`

        * Parameters:

            * `client_id` - Client ID

            * `client_secret` - Client Secret

            * `grant_type`
                * `password` - Password authorization
                    * Example:

                        ```curl -X POST -d "client_id=<client_id>&client_secret=<client_secret>&grant_type=password&username=<user_name>&password=<password>" http://localhost:8000/api/auth/token```

                * `refresh_token` - Refresh token
                    * Example:

                        ```curl -X POST -d "grant_type=refresh_token&client_id=<client_id>&client_secret=<client_secret>&refresh_token=<your_refresh_token>" http://localhost:8000/api/auth/token```

            * `username` - Only used with `password` grant_type

            * `password` - Only used with `password` grant_type

    * **Convert 3rd party token to local**: [/api/auth/convert-token/](/api/auth/convert-token/)
        Use this endpoint to convert 3rd party (eg facebook tokens to local tokens). After that, you'll only need
        to use the local token. Please note the token expiration and request `refresh_token` if it's expired.

        Example: `curl -H "Authorization: Bearer facebook <backend_token>" /api/auth/convert-token`

        * Allowed methods

            * `GET`


    ___

    ## Reports:
    * List: [/api/reports/](/api/reports/)

    * Detail: [/api/reports/<id\>/](/api/reports/<id>/)

    * Counts: [/api/reports/counts/](/api/reports/counts/)

    ___

    ## Current User Information:
    * Detail: [/api/user/](/api/user/)

    ___

    ## Wards:
    * List: [/api/wards/](/api/wards/)

    * Detail: [/api/wards/<id\>/](/api/wards/<id>/)

    ___

    ## Categories:
    * List: [/api/categories/](/api/categories/)

    * Detail: [/api/categories/<id\>/](/api/categories/<id>/)

    ___

    ## FAQ:
    * List: [/api/faq/](/api/faq/)


    ___

    ## Contact:
    * Form: [/api/contact/](/api/contact/)


    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        data = Response({
        })

        return data


class ReportListCreateView(generics.ListCreateAPIView):
    """
    List of all reports. Dates are UTC.

    ##**Available filters**:

    (All filters are optional)

    * `center_point` - Longitude and latitude of center separated by comma (e.g. 44.789856649281205,41.72166021377742).
    Used in conjunction with `center_distance`, to filter reports from the center up to provided distance in meters
    * `center_distance` - Distance from `center_point`. In order to enable this filtering, both `center_point` and
    `center_distance` must be provided
    * `status` - Report status. You can get available statuses by using OPTIONS request on this endpoint
    * `category` - Category by id
    * `start_date` Min date in unix timestamp (utc)
    * `end_date` - Max date in unix timestamp (utc)
    * `has_photo` - Bool.
    * `ward__city` - City ID. You can get city ID from [/api/wards/](/api/wards/)
    * `user_id` - User ID. You can get user ID from [/api/user/](/api/user/)

    ##**Sorting**:

    * `order_by`

        * `created_at` - Oldest first
        * `-created_at` - Newest first

    **Example**: [/api/reports/?category=25&status=fixed&order_by=created_at](/api/reports/?category=25&status=fixed&has_photo=true&order_by=created_at)

    -----
    """
    queryset = Report.active.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ReportSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_class = ReportFilter
    ordering_fields = ('created_at',)

    def get_queryset(self):
        queryset = self.queryset
        center_point = self.request.QUERY_PARAMS.get('center_point', None)
        center_distance = self.request.QUERY_PARAMS.get('center_distance', None)
        start_date = self.request.QUERY_PARAMS.get('start_date', None)
        end_date = self.request.QUERY_PARAMS.get('end_date', None)
        has_photo = self.request.QUERY_PARAMS.get('has_photo', None)
        user_id = self.request.QUERY_PARAMS.get('user_id', None)

        if center_distance and center_point:
            center_point = center_point.replace(',', ' ')
            center_point = fromstr('POINT({0})'.format(center_point), srid=4326)
            queryset = queryset.filter(point__distance_lte=(center_point, D(m=center_distance)))

        if start_date:
            start_date = datetime.datetime.fromtimestamp(int(start_date))
            min_day = datetime.datetime.combine(start_date, datetime.time.min)
            queryset = queryset.filter(created_at__gte=min_day)

        if end_date:
            end_date = datetime.datetime.fromtimestamp(int(end_date))
            max_day = datetime.datetime.combine(end_date, datetime.time.max)
            queryset = queryset.filter(created_at__lte=max_day)

        if has_photo:
            if has_photo.lower() == 'true' or '1':
                queryset = queryset.exclude(photo__isnull=True).exclude(photo="")
            else:
                queryset = queryset.filter(photo="")

        if user_id:
            queryset = queryset.filter(user__id=int(user_id))

        return queryset


class ReportDetailView(APIView):
    model = Report

    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        report = self.get_object(pk)
        serializer = ReportSerializer(report)
        return Response(serializer.data)

class ExtendedUserDetailView(generics.GenericAPIView):
    serializer_class = ExtendedUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class CategoryListView(generics.ListAPIView):
    queryset = ReportCategory.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(APIView):
    model = ReportCategory

    def get_object(self, pk):
        try:
            return ReportCategory.objects.get(pk=pk)
        except ReportCategory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)


class WardListView(generics.ListAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer


class FaqEntryListView(generics.ListAPIView):
    queryset = FaqEntry.objects.all().order_by('order')
    serializer_class = FaqEntrySerializer


class WardDetailView(APIView):
    model = Ward

    def get_object(self, pk):
        try:
            return Ward.objects.get(pk=pk)
        except Ward.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ward = self.get_object(pk)
        serializer = WardSerializer(ward, context={'request': request})
        return Response(serializer.data)


class ObtainAuthTokenView(ObtainAuthToken):
    """
    Obtain authentication token.

    Make sure to clear session cookies if you have them, otherwise authentication will fail and you'll get an CSRF error.
    """
    metadata_class = AuthTokenMetaData

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = FMSUserAuthToken.objects.get_or_create(user=user)
        return Response({'token': token.token})


class ReportCountView(APIView):
    permission_classes = (permissions.AllowAny,)
    metadata_class = ReportCountMetadata

    def get(self, request):
        report_count = ReportCount.by_interval('1 year')
        counts = OrderedDict({
            'total': report_count.get_counts(),
            'fixed': report_count.fixed().get_counts(),
            'not-fixed': report_count.not_fixed().get_counts(),
            'in-progress': report_count.in_progress().get_counts()
        })
        return Response(counts)

class ContactFormRenderer(BrowsableAPIRenderer):
    def get_context(self, *args, **kwargs):
        context = super(ContactFormRenderer, self).get_context(*args, **kwargs)
        context["post_form"] = ContactForm(initial=context['request'].data)
        return context

@renderer_classes((ContactFormRenderer,JSONRenderer))
class ContactView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer = ContactSerializer

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'detail': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
