from django import forms
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import get_language, ugettext_lazy as _

from apps.mainapp.models import Report, ReportUpdate, ReportSubscriber, ReportCategory
from apps.users.models import FMSUser


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control required', 'placeholder': _('Name')}),
                           label="")
    email = forms.EmailField(widget=forms.TextInput(attrs=dict({'class': 'form-control required',
                                                                'placeholder': _('Email')},
                                                               maxlength=200)),
                             label="")
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-margin-fix required', 'rows': '5', 'cols': '20',
                                     'placeholder': _('Message')}),
        label="")

    def save(self, fail_silently=False):
        message = render_to_string("emails/contact/message.txt", self.cleaned_data)
        send_mail('FixMyStreet.ge User Message from %s' % self.cleaned_data['email'], message,
                  settings.EMAIL_FROM_USER, [settings.ADMIN_EMAIL], fail_silently=False)


class ReportUpdateForm(forms.ModelForm):
    error_messages = {
        'login_required': _('You need to be logged in to post an update'),
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReportUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ReportUpdate
        fields = ('desc', 'photo', 'status')

    def clean(self):
        clean_data = super(ReportUpdateForm, self).clean()
        status = self.cleaned_data.get('status')
        if not self.user.is_authenticated():
            raise forms.ValidationError(self.error_messages['login_required'], code='login_required')
        return clean_data


class ReportSubscriberForm(forms.ModelForm):
    class Meta:
        model = ReportSubscriber
        fields = ('email',)


class ReportForm2(forms.ModelForm):
    """
    2nd step of form submission
    """
    category = forms.ModelChoiceField(queryset=ReportCategory.objects.all().order_by('name_' + get_language()[:2]),
                                      label=_('Category'))
    error_messages = {
        'password_insecure': _('Password should contain at least 8 characters, 1 alpha numeric and 1 digit'),
        'duplicate_username': _("User with that username already exists."),
        'not_confirmed': _("Account is not confirmed. Confirmation email has been resent")
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReportForm2, self).__init__(*args, **kwargs)
        # We don't need user creation fields if user is already logged in
        if not self.user.is_authenticated():
            self.fields['username'] = forms.CharField(label=_('Username'), max_length=30)
            self.fields['password1'] = forms.CharField(widget=forms.PasswordInput, label=_('Password'),)
            self.fields['password2'] = forms.CharField(widget=forms.PasswordInput, label=_('Repeat Password'))

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

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(_("Passwords don't match!"))
        if len(password2) < 8:
            raise forms.ValidationError(self.error_messages['password_insecure'], code='password_insecure')
        if not any(char.isdigit() for char in password2):
            raise forms.ValidationError(self.error_messages['password_insecure'], code='password_insecure')
        if not any(char.isalpha() for char in password2):
            raise forms.ValidationError(self.error_messages['password_insecure'], code='password_insecure')

        return password2

    class Meta:
        model = Report
        fields = ('desc', 'photo', 'category')


class ReportForm1(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small',
            'placeholder': _("Problem Title")
        }))

    street = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small',
            'placeholder': _("Street")
        }))

    first_name = forms.CharField(required=False,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'required form-control input-small user-hidden',
                                         'placeholder': _("First Name")
                                     }))

    last_name = forms.CharField(required=False,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'required form-control input-small user-hidden',
                                        'placeholder': _("Last Name")
                                    }))

    phone = forms.CharField(required=False,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'required form-control input-small user-hidden',
                                    'placeholder': _("Phone Number")
                                }))
    email = forms.EmailField(required=False,
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'required form-control input-small user-hidden',
                                     'placeholder': _("Email"),
                                     'type': 'hidden',
                                 }))
    lon = forms.CharField(widget=forms.TextInput(attrs={'class': 'required', 'type': 'hidden'}))
    lat = forms.CharField(widget=forms.TextInput(attrs={'class': 'required', 'type': 'hidden'}))


class sortingForm(forms.Form):
    CHOICES = (('-created_at', _('Created descending')),
               ('created_at', _('Created ascending')),
               ('-sub_count', _('Most subscribers')),
    )
    sorting = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'class': ''}), choices=CHOICES)
