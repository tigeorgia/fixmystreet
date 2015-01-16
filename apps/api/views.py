from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse as dj_reverse
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse as reverse
from django.http import Http404
from collections import OrderedDict

from apps.mainapp.models import Report, Ward
from apps.mainapp.filters import ReportFilter
from .serializers import ReportSerializer, WardSerializer, AuthTokenSerializer
from metadata import ReportMetaData, AuthTokenMetaData


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
    HTTP header, prepended with the string "Token ".  For example:

    `Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a`

    # Endpoints:
    ## Authorization:
    Obtain token: [/api/get-token/](/api/get-token/)

    ## Reports:
    List: [/api/reports/](/api/reports/)

    Detail: [/api/reports/<id\>/](/api/reports/<id>/)


    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        data = Response({
        })

        return data


class ReportListCreateView(generics.ListCreateAPIView):
    """
    List of all reports.

    ##**Available filters**:

    `status` \n
    `category` \n
    `from_date` \n
    `to_date` \n
    `ward__city` \n

    **Example**: [/api/reports/?category=25&status=fixed](/api/reports/?category=25&status=fixed)

    ##**Sorting**:


    -----
    """
    queryset = Report.active.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReportSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    metadata_class = ReportMetaData
    filter_class = ReportFilter
    ordering_fields = ('created_at',)


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
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})