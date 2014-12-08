from django.views.generic import View, FormView
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth import views, login as auth_login
from django.views.decorators.csrf import csrf_protect
import json

from .models import FMSUser
from .forms import FMSUserLoginForm


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


class AjaxLoginView(View):
    form_class = FMSUserLoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)

        if form.is_valid() and request.is_ajax():
            auth_login(request, form.get_user())
            return JsonResponse(data={'success': True})
        else:
            errors = {'errors': [e for e in form.errors['__all__']]}
            return JsonResponse(errors)