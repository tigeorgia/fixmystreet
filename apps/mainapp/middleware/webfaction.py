from django.conf import settings

class WebFactionFixes(object):
    """Sets 'REMOTE_ADDR' based on 'HTTP_X_FORWARDED_FOR', if the latter is
    set.
    """
    def process_request(self, request):
        if settings.WEBFACTION:
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
                request.META['REMOTE_ADDR'] = ip
                del request.META['HTTP_X_FORWARDED_FOR']