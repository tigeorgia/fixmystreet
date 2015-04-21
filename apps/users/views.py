from django.views.generic import View, FormView, TemplateView, CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.contrib.auth import login as auth_login
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib import messages

from .models import FMSUser, FMSUserTempToken
from .signals import user_confirmed
from utils.utils import get_client_ip
import forms


class RegistrationView(CreateView):
    model = FMSUser
    form_class = forms.FMSUserCreationForm
    success_url = '/'
    template_name = 'users/register.html'
    messages = {'success': _('Signup was successful. Please check your email for verification')}

    def form_invalid(self, form):
        response = super(RegistrationView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'success': False,
                                 'errors': form.errors.as_json(escape_html=True)})
        else:
            return response

    def form_valid(self, form):
        response = super(RegistrationView, self).form_valid(form)
        if self.request.is_ajax():
            return JsonResponse({'success': True,
                                 'message': self.messages['success']})
        else:
            return response


class AjaxLoginView(View):
    form_class = forms.FMSUserLoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)

        if form.is_valid() and request.is_ajax():
            auth_login(request, form.get_user())
            return JsonResponse(data={'success': True})
        else:
            errors = {'errors': [e for e in form.errors['__all__']]}
            return JsonResponse(errors)


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = forms.FMSUserLoginForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return super(LoginView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class TokenConfirmationView(TemplateView):
    template_name = 'users/email_confirm.html'

    def get_context_data(self, **kwargs):
        context = super(TokenConfirmationView, self).get_context_data(**kwargs)
        try:
            user = FMSUser.objects.get(fms_user_token__token=kwargs['token'])
        except FMSUser.DoesNotExist:
            context['message'] = _('Invalid confirmation link')
        else:
            user.is_confirmed = True
            user.fms_user_token.delete()
            user.save()
            user_confirmed.send(sender=self.__class__, user=user)
            context['message'] = _('Confirmation successful! You can now login')

        return context


class PasswordResetView(FormView):
    form_class = forms.PasswordResetStart
    template_name = 'users/reset.html'
    model = FMSUserTempToken
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(PasswordResetView, self).get_context_data(**kwargs)
        context['message'] = _('Please enter your email')
        return context

    def send_email(self):
        url = self.object.get_absolute_url()
        subject = _('Password confirmation')
        message = render_to_string('users/reset_confirm.txt',
                                   {'user': self.object.user, 'reset_url': url}
                                   )
        self.object.user.email_user(subject=subject, message=message)

    def form_valid(self, form):
        token_obj = self.model.get_unused_token(form.user)
        if not token_obj:
            token_obj = self.model.objects.create(user=form.user)
            token_obj.ip = get_client_ip(self.request)
            token_obj.save()

        self.object = token_obj
        self.send_email()
        messages.success(self.request, _('Please check email associated with the account for password reset link'))
        return HttpResponseRedirect('/')


class PasswordResetConfirmView(FormView):
    form_class = forms.PasswordResetConfirm
    template_name = 'users/reset.html'
    model = FMSUserTempToken
    success_url = reverse_lazy('users:login')
    object = None  # Token object

    def update_token(self):
        self.object.used = True
        self.object.used_ip = get_client_ip(self.request)
        self.object.save()

    def check_token(self):
        try:
            token_obj = self.model.objects.get(pk=self.kwargs['token'])
        except self.model.DoesNotExist:
            raise Http404(_("Incorrect reset link"))
        if token_obj.used:
            raise Http404(_("Incorrect reset link"))
        else:
            self.object = token_obj

    def get_context_data(self, **kwargs):
        context = super(PasswordResetConfirmView, self).get_context_data(**kwargs)
        context['message'] = _('Please enter your new password')
        return context

    def get(self, request, *args, **kwargs):
        self.check_token()
        return super(PasswordResetConfirmView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.check_token()
        user = self.object.user
        user.set_password(form.cleaned_data['password1'])
        user.save()
        messages.success(self.request, _('Password updated. You can log in now.'))
        self.update_token()
        return super(PasswordResetConfirmView, self).form_valid(form)