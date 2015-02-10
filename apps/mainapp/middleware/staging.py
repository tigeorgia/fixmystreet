from django.conf import settings
from django.core.exceptions import PermissionDenied

class RestrictStagingAccess(object):
    def process_request(self, request):
        if settings.STAGING and request.META['REMOTE_ADDR'] not in settings.STAGING_ACCESS:
                raise PermissionDenied