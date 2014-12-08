from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

from apps.users.models import FMSUser


class FMSUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(FMSUserCreationForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            FMSUser.objects.get(username=username)
        except FMSUser.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    class Meta:
        model = FMSUser
        fields = ('username', 'first_name', 'last_name', 'email')


class FMSUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(FMSUserChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FMSUser
        fields = ('username', 'first_name', 'last_name', 'email')


class FMSCheckEmailForm(forms.Form):
    email = forms.EmailField(label=_('Email'))


class FMSUserLoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(FMSUserLoginForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].label = _('Email')
        self.fields['username'].widget = forms.TextInput(attrs={'type': 'email', 'id': 'login_email',
                                                                'readonly': True})
        self.error_messages['invalid_login'] = _('Incorrect email address or password')