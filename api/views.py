from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404

from mainapp.models import Report
from serializers import ReportSerializer


class LoginRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        redirect_url = reverse('home')

        if 'api' in self.request.path and self.request.user.apiuser.api_read:
            redirect_url = reverse('api:reports')

        elif self.request.user.is_staff:
            redirect_url = reverse('admin')

        return redirect_url


class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReportSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class ReportDetail(APIView):
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        report = self.get_object(pk)
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        report = self.get_object(pk)
        serializer = ReportSerializer(report, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
