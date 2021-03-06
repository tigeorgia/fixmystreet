from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Field, MultiField, ButtonHolder
from crispy_forms.bootstrap import InlineField, StrictButton

from apps.users.models import FMSUser, FMSUserTempToken
from apps.users.validators import FMSUserValidators


class FMSUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    def __init__(self, *args, **kwargs):
        self.user_validators = FMSUserValidators()
        super(FMSUserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
                'username',
                'email',
                Div(
                    Div('first_name', css_class='col-md-6 col-sm-6'),
                    Div('last_name', css_class='col-md-6 col-sm-6'),
                    css_class='row row-no-margin',
                ),
                'phone',
                Div(
                    Div('password1'),
                    Div('password2'),
                ),
            ButtonHolder(
                StrictButton(_('Register'), css_class='btn btn-default btn-block btn-lg', type='submit')
            )
        )

    class Meta:
        model = FMSUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']

    def clean(self):
        cleaned_data = self.cleaned_data
        self.user_validators.validate(**cleaned_data)
        return self.cleaned_data

    def save(self, commit=True):
        user = super(FMSUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class FMSUserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_validators = FMSUserValidators()
        super(FMSUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
                'username',
                'email',
                Div(
                    Div('first_name', css_class='col-md-6 col-sm-6'),
                    Div('last_name', css_class='col-md-6 col-sm-6'),
                    css_class='row row-no-margin',
                ),
                'phone',
            ButtonHolder(
                StrictButton(_('Update'), css_class='btn btn-default btn-block btn-lg', type='submit')
            )
        )

    class Meta:
        model = FMSUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

    def clean(self):
        username = self.cleaned_data.get('username')
        if self.instance.username != username:
            self.user_validators.validate_username(username)
        return self.cleaned_data


class FMSCheckEmailForm(forms.Form):
    email = forms.EmailField(label=_('Email'))


class FMSUserLoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(FMSUserLoginForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].label = _('Email')
        self.fields['username'].widget = forms.TextInput(attrs={'type': 'email', 'id': 'login_email'})
        self.error_messages['invalid_login'] = _('Incorrect email address or password')
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
                'username',
                'password',
            ButtonHolder(
                StrictButton(_('Login'), css_class='btn btn-default btn-block btn-lg', type='submit')
            )
        )

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class PasswordResetStart(forms.Form):
    email = forms.EmailField(label=(_('Email')))
    captcha = ReCaptchaField(attrs={'theme': 'clean'}, label=_('Captcha'))

    def __init__(self, *args, **kwargs):
        super(PasswordResetStart, self).__init__(*args, **kwargs)
        self.validators = FMSUserValidators()
        self.user = None
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
                'email',
                'captcha',
            ButtonHolder(
                StrictButton(_('Request reset link'), css_class='btn btn-default btn-block btn-lg', type='submit')
            )
        )

    def clean(self):
        email = self.cleaned_data.get('email')
        user = FMSUser.get_user_by_email(email)
        if not user:
            raise forms.ValidationError(_('User with provided email not found'))
        else:
            self.user = user
        return self.cleaned_data

class PasswordResetConfirm(forms.Form):
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    def __init__(self, *args, **kwargs):
        super(PasswordResetConfirm, self).__init__(*args, **kwargs)
        self.user_validators = FMSUserValidators()
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
                'password1',
                'password2',
            ButtonHolder(
                StrictButton(_('Reset password'), css_class='btn btn-default btn-block btn-lg', type='submit')
            )
        )

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        self.user_validators.validate_passwords(password1, password2)
        return self.cleaned_data
