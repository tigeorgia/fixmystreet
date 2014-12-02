from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from .models import FMSUser


class EmailExistsView(View):
    http_method_names = ['get']

    def _email_exists(self, email):
        try:
            user = FMSUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return False

        return True

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        response = {'email_exists': True if self._email_exists(email) else False}
        return JsonResponse(response)
